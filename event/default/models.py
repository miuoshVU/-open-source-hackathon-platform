from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin
from .managers import CustomUserManager
from .choices import *
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):

    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    joined_discord = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    phone_verification_code = models.CharField(max_length=6, blank=True, null=True)

    timestamp = models.DateTimeField(null=True, blank=True)

    source = models.TextField(null=True, blank=True, default="")

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country_code = models.CharField(default="", max_length=32, blank=False, choices=country_code_choices)
    phone = models.CharField(max_length=15)
    city = models.CharField(
        default="", max_length=75, null=False, blank=False)
    country = models.CharField(
        default="", max_length=60, blank=False, choices=country_choices)
    project_url = models.TextField(null=False, blank=False, max_length=200)
    issue_desc = models.TextField(null=False, blank=False)
    project_info = models.TextField(null=False, blank=False)
    project_impact = models.TextField(null=False, blank=False)
    contribution_url = models.TextField(null=False, blank=False, max_length=200)
    feedback = models.TextField(null=True, blank=True, default="")
    expertise = models.TextField(null=True, blank=True, default="")
    interest = models.TextField(null=True, blank=True, default="")
    team = models.TextField(null=True, blank=True, default="")
    profile_url = models.TextField(null=True, blank=True, max_length=200, default="")
    hackathon = models.TextField(null=True, blank=True, max_length=200, default="")
    coder_password = models.TextField(null=True, blank=True, max_length=200, default="")
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Referer(models.Model):
    
    referer = models.TextField(null=True, blank=True, default="")
    click_source = models.TextField(null=True, blank=True, default="")


class Event(models.Model):

    title = models.CharField(max_length=120, blank=False, null=False)
    description = models.CharField(max_length=200, blank=False, null=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField()

    def __str__(self):
        return self.title + str(self.date) + str(self.start_time) + '-' + str(self.end_time)


class OtpCode(models.Model):

    otpcode = models.CharField(max_length=6)


class IncomingPhoneNo(models.Model):

    From = models.CharField(max_length=18)
    FromCity = models.CharField(max_length=18)
    FromCountry = models.CharField(max_length=18)
    Caller = models.CharField(max_length=18)
    CallerCity = models.CharField(max_length=18)
    CallerCountry = models.CharField(max_length=18)
    time = models.DateTimeField(default=timezone.now, blank=True)