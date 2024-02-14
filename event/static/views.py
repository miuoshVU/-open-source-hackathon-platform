
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, HackerCreationForm, PhoneVerificationForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, authenticate
from .helper import add_group
from .emailer import *
from .decorators import user_not_authenticated

from twilio.rest import Client
account_sid = 'AC9cef4f76fdda9c88bda8b03ef16cb4d1'
auth_token = 'b4440e9d1b2bb679fd0f35ebff37ca44'
client = Client(account_sid, auth_token)
import logging

# Add this at the top of your views.py file
logger = logging.getLogger(__name__)

@user_not_authenticated
def registration(request):
    if request.method == 'POST':
        create_user_form = CustomUserCreationForm(request.POST, request.FILES)
        create_hacker_form = HackerCreationForm(request.POST)
        if create_hacker_form.is_valid() and create_user_form.is_valid():
            pword = create_user_form.cleaned_data['password1']

            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            country = request.POST.get('country')
            user = create_user_form.save()

            phone = request.POST.get('phone')

            # ------------------------------------------------------
            user = create_user_form.save(commit=False)
            email = create_user_form.cleaned_data['email'].lower()
            user.email = email
            user.save()
            # Send activation email
            activateEmail(request, user, create_user_form.cleaned_data.get('email'))
            # Generate token
            token = default_token_generator.make_token(user)
            print(f"User Token is: {token}")

            user.phone = phone
            code_to_generate_for_phone_verifi = generate_random_code()
            print("--------------------------------------------------")
            print(code_to_generate_for_phone_verifi)
            send_sms(code_to_generate_for_phone_verifi,phone)
            user.phone_verification_code = code_to_generate_for_phone_verifi
            user.save()

            hacker = create_hacker_form.save(commit=False)
            hacker.user = user
            hacker.save()
            add_group(user, 'hacker')

            print()
            user = authenticate(request, username=user.email, password=pword)
            if user is not None:
                login(request, user)
                return redirect('landing')
        else:
            for error in list(create_user_form.errors.values()):
                messages.error(request, error)
    else:
        create_user_form = CustomUserCreationForm()
        create_hacker_form = HackerCreationForm()

    context = {'create_hacker_form': create_hacker_form,
               'create_user_form': create_user_form}
    return render(request, 'defaults/register.html', context)

def send_sms(user_code, phone):
    message = client.messages.create(
        body=f"Hi! Your user and verification code is {user_code}",
        from_='<phone_number>',
        to=f'{phone}'
    )

    print(message.sid)

def verify_phone(request):
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)

        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            print(entered_code)
            print(request.user)
            print(request.user.is_phone_verified)
            # Compare the entered code with the stored code
            if request.user.phone_verification_code == entered_code:
                # Update the phone_is_verified field
                request.user.is_phone_verified = True
                request.user.save()
                messages.success(request, "Phone number verified successfully.")
                return redirect('login')
            else:
                messages.error(request, "Invalid verification code.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = PhoneVerificationForm()

    return render(request, 'defaults/verify_phone.html', {'form': form})

def generate_random_code():

    import secrets
    return secrets.randbelow(10000)
