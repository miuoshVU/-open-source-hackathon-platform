# This file sends emails from the default app
from django.core.mail import send_mail
from django.template.loader import render_to_string
from event.settings.base import EMAIL_OUTGOING

import os

TEAM_NAME="Parkyeri Christmas Challenge Team"
FROM_EMAIL= EMAIL_OUTGOING

def test_mail():
    print("test email")
    subject = "Testing mail"
    from_email=FROM_EMAIL
    body = '''
     Hey yo what's good dawg
    '''
    to_email = ['fj@gmail.com']

    send_mail(subject=subject, from_email=from_email,
              recipient_list=to_email, message=body, fail_silently=False)


def password_reset_instructions(domain, user, uid, token):
    subject = "Christmas Challenge Reset Password Link"
    from_email=FROM_EMAIL
    to_email=[user.email]
    email_variables = {
        "domain":domain,
        "uid": uid,  
        "user": user,
        "token": token,
        "team_name":TEAM_NAME,
    }

    body = render_to_string('defaults/resetpassword.txt', email_variables)

    send_mail(subject=subject, from_email=from_email, 
                recipient_list=to_email, message=body,fail_silently=False)

def password_reset_success(user):
    subject = "You've successfully reset your password!"
    from_email=FROM_EMAIL
    to_email = [user.email]
    body = '''
        Hey! You've successfully reset your password! 

        Thanks!
        {}
    '''.format(TEAM_NAME)

    send_mail(subject=subject, from_email=from_email,
              recipient_list=to_email, message=body, fail_silently=False)

def registration_confirmation(hacker):
    subject = "{}, you've successfully registered for Christmas Challenge (YAY!)".format(hacker.first_name)
    from_email=FROM_EMAIL
    to_email=[hacker.email]
    body = '''
        Hey {},

        We've received your application for Christmas Challenge!

        See you in our discord channel!
        {}
    '''.format(hacker.first_name,TEAM_NAME)

    send_mail(subject=subject, from_email=from_email,
              recipient_list=to_email, message=body, fail_silently=False)


def hacker_checkin_success(hacker):
    subject = "{}, you have checked in at Christmas Challenge!".format(hacker.first_name)
    from_email=FROM_EMAIL
    to_email = [hacker.email]
    body = '''
    Hey {}, 

    Thanks for coming out this weekend to have a blast at Christmas Challenge. We've checked you in to our system. 
    Please check out the website for the event schedule and we can't wait to see you at the opening ceremony!

    Best,
    
    '''.format(hacker.first_name, TEAM_NAME)


    send_mail(subject=subject, from_email=from_email,
              recipient_list=to_email, message=body, fail_silently=False)


def new_organizer_added(link, organizer):
    subject = "{}, you have been added to Christmas Challenge as an Organizer".format(
        organizer.first_name)
    from_email=FROM_EMAIL
    to_email = [organizer.email]
    body = '''
    Hey {}, 
        You've been added to the system as an organizer. You got some powers like checking in hackers.
        Your login credentials are associated with this email. You already know the password ;) 
        Please reset your password {}
   
        -{}
    '''.format(organizer.first_name, link, TEAM_NAME)


    send_mail(subject=subject, from_email=from_email,
              recipient_list=to_email, message=body, fail_silently=False)
