import subprocess
from .coder_api import coder_api
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activate_token
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from .models import HackerInfo
from default.forms import CustomUserChangeForm
from default.models import CustomUser, IncomingPhoneNo
from default.views import clean_country_code
from .forms import ChangePhoneForm
import hashlib
from django.contrib import messages
import json

# for email verification
# for phone verification
from .forms import PhoneVerificationForm
# twilio verification settings
twilio_auth_code = "<auth_code>"
twilio_api_url = "https://api.twilio.com/endpoint"
twilio_from_phone = "<phone_number>"

def dash(request):
    user = request.user
    hacker = HackerInfo.objects.get(user=request.user)
    first_name_hash = hashlib.sha256(
        hacker.user.first_name.encode()).hexdigest()
    last_name_hash = hashlib.sha256(hacker.user.last_name.encode()).hexdigest()
    # ----------------------------------------
    if request.method == "POST" and 'phone-btn' in request.POST:
        if (user.is_phone_verified):
            messages.info(request, "Your phone is already verified!")
        else:
            return redirect('verify-by-call')
    # ----------------------------------------
    if request.method == "POST" and 'email-btn' in request.POST:
        if (user.is_email_verified):
            messages.info(request, "Your email is already verified!")
        else:
            activate_email(request, user, user.email)
            # token = default_token_generator.make_token(user)
    # ----------------------------------------
    if request.method == "POST" and 'container-btn' in request.POST:
        activate_container(request, user)
    # ----------------------------------------
    user_change_form = CustomUserChangeForm(instance=user)
    check_in_url = "{}/check-in/{}/{}/{}".format(
        request.get_host(), first_name_hash, last_name_hash, hacker.user.id)
    context = {'check_in_url': check_in_url,
                'user_change_form': user_change_form, 'user': user}
    if not user.is_email_verified:
        messages.info(request, "You must verify your email address!")
    return render(request, 'hackers/dashboard.html', context)

# ----------------------------------------


def activate(request, uidb64, token):  # email verification
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.success(
            request, "Your email is now verified.")
        return redirect('hacker-dash')
    else:
        messages.error(request, "Activation link is invalid!")
    return redirect('hacker-dash')

def update_checkbox(request):
    if request.method == 'POST':
        if request.method == "POST":
            checked = request.POST.get('myCheckbox')
            user = CustomUser.objects.get(pk=request.user.id)
            if user.joined_discord:
                user.joined_discord = False
            else:
                user.joined_discord = True
            user.save()
    return redirect('hacker-dash')


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
    try:
        email.send()
        messages.info(request, f'Dear participant, please check your email and click on \
            the activation link to complete the verification step.<br/>Note: Check your spam folder as well.')
    except Exception as e:
        email = EmailMessage(mail_subject, text_message, to=[to_email])
        email.send()


# ----------------------------------------
def activate_container(request, user):  # container activation
    coder_user = coder_api.get_coder_user(user.email)
    print(f"starting activate with coder_user={coder_user} coder_password={user.coder_password}")
    if coder_user is None or user.coder_password is None or user.coder_password=="":
        if coder_user is None:
            coder_username = user.email.split("@")[0] # get first part of username
            coder_user = coder_api.create_coder_user(user.email, coder_username,nicepass(9,5))
            if coder_user is None:
                coder_username = user.email.replace("@","-").replace(".","-")
                new_coder_user = coder_api.create_coder_user(user.email, coder_username,nicepass(9,5))
                coder_user = coder_api.get_coder_user(user.email)
                if coder_user is None:
                    messages.warning(request, "Failed to create container account. Please get help on our discord channel.")
                    return

            messages.info(request, "Your coder space is now activated!")
    random_pass = nicepass(9,5)
    if coder_api.set_password(coder_user,random_pass):
        user.coder_password = random_pass
        messages.info(request, "Your coder space password has been set!")
    else:
        messages.warning(request, "Failed to set your password for the code server. Please get help on  our discord channel.")
        user.coder_password = ""
    user.save()

def generate_random_code():  # phone verification
    from random import randint
    return randint(100000, 999999)

def is_expired(timestamp):
        return timezone.now() == timestamp

def cURL(request, country_code, phone):  # phone verification
    otp_code = generate_random_code()
    curl_command = ['curl',
        twilio_api_url,
        '-X', 'POST',
        '--data-urlencode', f'To=+{country_code+phone}',
        '--data-urlencode', f'From=+{twilio_from_phone}',
        '--data-urlencode', f'Body=Parkyeri Challenge verification code is: {otp_code}',
        '-u', twilio_auth_code]
    output = subprocess.check_output(curl_command, stderr=subprocess.STDOUT)
    response = output.decode("utf-8")
    response = response.split('\n')
    response = response[3]
    response = json.loads(response)
    if response["status"] == "queued":
        request.user.timestamp = timezone.now()
        request.user.phone_verification_code = otp_code
        request.user.save()
        messages.success(
            request, "A verification code has been sent to your account.")
    else:
        messages.error(
            request, "There was a problem sending verification code to your phone. Please try again and check your phone number!")

def verify_by_otp(request):  # phone verification
    if (request.user.is_phone_verified):
        messages.error(request, "Your phone number is already verified.")
        return redirect('hacker-dash')
    else:
        if request.method == "POST" and 'phone-btn' in request.POST:
            changePhoneForm = ChangePhoneForm(request.POST, instance=request.user)
            if changePhoneForm.is_valid():
                if(check_phone_availability(request)):
                    country_code = changePhoneForm.cleaned_data['country_code']
                    country_code = clean_country_code(country_code)
                    if request.user.timestamp is None:
                        changePhoneForm.save()
                        cURL(request, country_code, changePhoneForm.cleaned_data['phone'])
                    elif request.user.timestamp + timedelta(hours=8) < timezone.now():
                        changePhoneForm.save()
                        cURL(request, country_code, changePhoneForm.cleaned_data['phone'])
                    else:
                        calculate_time = timedelta(hours=8)-(timezone.now()-request.user.timestamp)
                        hours = calculate_time.days * 24 + calculate_time.seconds // 3600
                        minutes = (calculate_time.seconds % 3600) // 60
                        if hours == 0:
                            messages.info(request, f"Verification code has already been sent to your number!<br/>You need to wait {minutes} more minutes to receive a new verification code!")
                        else:
                            messages.info(request, f"Verification code has already been sent to your number!<br/>You need to wait {hours} hours and {minutes} minutes to receive a new verification code!")
                else:
                    messages.info(request, f'Another user is already verified with this phone number. Please change your phone number.')

        if request.method == 'POST' and 'otp-btn' in request.POST:
            phoneVerificationForm = PhoneVerificationForm(request.POST)
            if phoneVerificationForm.is_valid():
                print(request.user.country_code)
                entered_code = phoneVerificationForm.cleaned_data['otpcode']
                if request.user.phone_verification_code == entered_code:
                    # Update the phone_is_verified field
                    request.user.is_phone_verified = True
                    request.user.save()
                    messages.success(
                        request, "Phone number verified successfully.")
                    return redirect('hacker-dash')
                else:
                    messages.error(request, "Invalid verification code.")
            else:
                messages.error(request, "Invalid form submission.")
        otp_form = PhoneVerificationForm()
        change_phone_form = ChangePhoneForm(instance=request.user)
        return render(request, 'phone_verification.html', {'otp_form': otp_form, 'change_phone_form': change_phone_form})

def verify_by_call(request):  # phone verification
    if (request.user.is_phone_verified):
        messages.info(request, "Your phone number is already verified.")
        return redirect('hacker-dash')
    else:
        if request.method == 'POST' and 'verify-success' in request.POST:
            changePhoneForm = ChangePhoneForm(request.POST, instance=request.user)
            if changePhoneForm.is_valid():
                if(check_phone_availability(request)):
                    changePhoneForm.save()
                    incomingPhoneNo = IncomingPhoneNo.objects.all()
                    user_phone=f"+{clean_country_code(request.user.country_code)}{request.user.phone}"
                    for record in incomingPhoneNo:
                        passed_minutes_since_call=((timezone.now()-record.time).total_seconds())/60
                        if (record.From == user_phone) or (record.Caller == user_phone):
                            if (passed_minutes_since_call < 4):
                                request.user.is_phone_verified = True
                                request.user.save()
                                messages.success(request, "Phone number verified successfully.")
                                return redirect('hacker-dash')
                    else:
                        messages.info(request, "Sorry! Your phone no. could not get verified! Please try using verification code.")
                        return redirect('verify-by-otp')
                else:
                    messages.info(request, f'Another user is already verified with this phone number. Please change your phone number.')
        if request.method == 'POST' and 'verify-unsuccess' in request.POST:
            return redirect('verify-by-otp')
        change_phone_form = ChangePhoneForm(instance=request.user)
        return render(request, 'verify_by_phone_call.html', {'change_phone_form': change_phone_form})


def guide(request):
    return render(request, 'hackers/guide.html')


def check_phone_availability(request):
    check_phone = request.user.phone
    check_country_code = request.user.country_code
    print("check_phone: "+check_phone)
    print("check_country_code: "+check_country_code)
    if (CustomUser.objects.filter(phone=check_phone,country_code=check_country_code,is_phone_verified=True).exists()):
        return False
    return True

# def send_sms(user_code, phone):  # phone verification with twilio
#     message = client.messages.create(
#         body=f"{user_code} is your Hackathon verification code",
#         from_='+16363240647',
#         to=f'{phone}'
#     )
#     print(message.sid)


# edited but was from https://code.activestate.com/recipes/410076-generate-a-human-readable-random-password-nicepass/
def nicepass(alpha=6, numeric=2):
    """
    returns a human-readble password (say rol86din instead of
    a difficult to remember K8Yn9muL )
    """
    import string
    import random

    vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    chars = list(string.ascii_letters + string.digits+ "----------!@$&*_+")
    consonants = [a for a in chars if a not in vowels]
    digits = string.digits

    ####utility functions
    def a_part(slen):
        ret = ""
        for i in range(slen):
            if i % 2 == 0:
                randid = random.randint(0, len(consonants)-1)  # number of consonants
                ret += consonants[randid]
            else:
                randid = random.randint(0, 4)  # number of vowels
                ret += vowels[randid]
        return ret

    def n_part(slen):
        ret = ""
        for i in range(slen):
            randid = random.randint(0, 9)  # number of digits
            ret += digits[randid]
        return ret

    ####
    fpl = alpha / 2
    if alpha % 2:
        fpl = int(alpha / 2) + 1
    lpl = alpha - fpl

    start = a_part(int(fpl))
    mid = n_part(numeric)
    end = a_part(int(lpl))

    return "P2%s%s%s!" % (start, mid, end)
