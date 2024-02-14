from django.http.response import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
import json
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, HackerCreationForm, CustomUserChangeForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .helper import add_group, decide_redirect, decide_type
from .emailer import *
from .models import CustomUser, Referer
from django.templatetags.static import static

from .decorators import user_not_authenticated

# incoming calls handling twilio
import datetime
from .models import IncomingPhoneNo
from twilio.twiml.voice_response import VoiceResponse
from django.http import HttpResponse

# first time email
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from hacker.tokens import account_activate_token


def landing(request):
    source = request.GET.get('source')
    root_url = request.build_absolute_uri('/')[:-1]
    referer = request.META.get('HTTP_REFERER')

    if (referer is not None) or (source != request.session.get('source')):
        if referer is not None:
            if not referer.startswith(root_url):
                referer = Referer(referer=request.META.get('HTTP_REFERER'), click_source=request.GET.get('source'))
                referer.save()
        else:
            referer = Referer(referer=None, click_source=request.GET.get('source'))
            referer.save()

    if source is not None:
        request.session['source'] = source

    context = {}

    return render(request, 'defaults/landing.html', context)


def rules(request):
    return render(request, 'defaults/rules.html')


def privacy_policy_view(request):
    pdf_url = static('pdf/privacy_policy.pdf')
    return redirect(pdf_url)


def code_of_conduct_view(request):
    pdf_url = static('pdf/code_of_conduct.pdf')
    return redirect(pdf_url)


def clean_country_code(country_code):
    start_index = country_code.find('+') + 1
    end_index = country_code.find(')', start_index)
    if start_index != -1 and end_index != -1:
        return country_code[start_index:end_index]
    else:
        return None


@user_not_authenticated
def registration(request):
    if request.method == 'POST':
        create_user_form = CustomUserCreationForm(request.POST, request.FILES)
        create_hacker_form = HackerCreationForm(request.POST)
        if create_hacker_form.is_valid() and create_user_form.is_valid():
            pword = create_user_form.cleaned_data['password1']
            user = create_user_form.save()
            if request.session.get('source') is not None:
                source = request.session.get('source')
                user.source = source
            phone = request.POST.get('phone')
            user.phone = phone
            email = create_user_form.cleaned_data['email'].lower()
            user = create_user_form.save(commit=False)
            user.email = email
            user.save()
            hacker = create_hacker_form.save(commit=False)
            hacker.user = user
            hacker.save()
            add_group(user, 'hacker')
            user = authenticate(request, username=user.email, password=pword)
            if user is not None:
                login(request, user)
                activate_email(request, user, user.email)
                return redirect('hacker-dash')
        else:
            pass
    else:
        create_user_form = CustomUserCreationForm()
        create_hacker_form = HackerCreationForm()
    context = {'create_hacker_form': create_hacker_form,
               'create_user_form': create_user_form}
    return render(request, 'defaults/register.html', context)


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email').lower()
        email = "".join(email.split())
        passwrd = request.POST.get('password')
        user = authenticate(request, email=email, password=passwrd)
        if user is not None and decide_type(user) == "hacker":
            user.save()
            login(request, user)
            return redirect('hacker-dash')
        elif user is not None and decide_type(user) == "head-organizer":
            login(request, user)
            return redirect('organizer-dash')
        else:
            messages.error(request, "Username or Password Incorrect")
    context = {}
    return render(request, 'defaults/login.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            user_email = password_reset_form.cleaned_data['email'].lower()
            user_obj_valid = CustomUser.objects.filter(
                email=user_email).exists()
            if user_obj_valid:
                user_obj = CustomUser.objects.get(email=user_email)
                uid = urlsafe_base64_encode(force_bytes(user_obj.pk))
                token = default_token_generator.make_token(user_obj)
                password_reset_instructions(
                    request.get_host(), user_obj, uid, token)
                return redirect('password_reset_done')
            else:
                messages.error(request, "Email could not be found!")
    password_reset_form = PasswordResetForm()
    context = {'password_reset_form': password_reset_form}
    return render(request, 'defaults/password_reset.html', context)


def logout_user(request):
    logout(request)
    return redirect('landing')  # TODO


def check_email(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        received_json = json.loads(body_unicode)
        data = received_json.get("data")
        email_value = data.get("email").lower()
        message = ""
        validity = True
        if (CustomUser.objects.filter(email=email_value).exists()):
            message = "This Email is Already Registered"
            validity = False
        data = {
            "valid": validity,
            "message": message
        }
        return JsonResponse(data)
    return JsonResponse({"valid": False}, status=200)


def check_password(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        received_json = json.loads(body_unicode)
        data = received_json.get("data")
        password_value = data.get("p1")
        try:
            validate_password(password_value)
        except ValidationError as e:
            data = {
                "valid": False,
                "errors": list(e)
            }
            return JsonResponse(data)
        data = {
            "valid": True,
            "errors": ""
        }
        return JsonResponse(data)
    return JsonResponse({"valid": False}, status=200)
    return redirect('landing')


def profile_page(request, pk):
    user = None
    try:
        user = CustomUser.objects.get(id=pk)
    except:
        return redirect(decide_redirect(request.user))
    if user != request.user:
        return redirect(decide_redirect(request.user))
    if any("Your Submission Updated!" in message.message for message in messages.get_messages(request)):
        messages.get_messages(request).used = True
    elif user.is_submitted is True:
        messages.info(
                request, "You have already applied for a prize. You can still update your submission before the deadline.")
    else:
        if not user.is_email_verified and not user.is_phone_verified:
            messages.info(
                request, "You can see the submission questions, however you will not be able to submit your answers until your phone number and email are verified!")
        elif not (user.is_email_verified):
            messages.info(
                request, "You can see the submission questions, however you will not be able to submit your answers until your phone number and email are verified!")
        elif not (user.is_phone_verified):
            messages.info(
                request, "You can see the questions now. You will not be able to submit your answers until your phone number is verified!")
        else:
            messages.success(
                request, "Please fill out these forms to apply for a prize.")
    is_hacker = True if decide_type(user) == "hacker" else False
    if request.method == "POST":
        user_change_form = CustomUserChangeForm(request.POST, instance=user)
        if user_change_form.is_valid():
            user.is_submitted = True
            user.save()
            user_change_form.save()
            if is_hacker:
                storage = messages.get_messages(request)
                for message in storage:
                    message.used = True
                messages.success(request, "Your Submission Updated!")
                return redirect('profile', pk=user.id)
            else:
                messages.success(request, "Profile updated!")
    user_change_form = CustomUserChangeForm(instance=user)
    country_code = clean_country_code(user.country_code)
    context = {"user_change_form": user_change_form, "country_code": country_code}
    if is_hacker:
        return render(request, 'defaults/profileH.html', context)
    return render(request, 'defaults/profileO.html', context)


def incoming_call(request):
    incomingPhoneNo = IncomingPhoneNo(
        From=request.GET['From'], 
        FromCity=request.GET['FromCity'], 
        FromCountry=request.GET['FromCountry'], 
        Caller=request.GET['Caller'], 
        CallerCity=request.GET['CallerCity'], 
        CallerCountry=request.GET['CallerCountry'])
    incomingPhoneNo.save()
    response = VoiceResponse()
    response.reject()
    return HttpResponse(str(response))

def activate_email(request, user, to_email):  # email verification
    mail_subject = "Activate your user account."
    html_message = render_to_string("template_activate_account.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        # 'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activate_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    text_message = render_to_string("template_activate_account_plain.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        # 'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activate_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMultiAlternatives(mail_subject, html_message, to=[to_email])
    email.attach_alternative(html_message, "text/html")
    # try:
    #     email.send()
    # except Exception as e:
    #     email = EmailMessage(mail_subject, text_message, to=[to_email])
    #     email.send()

