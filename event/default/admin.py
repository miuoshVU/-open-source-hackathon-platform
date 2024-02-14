from default.models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Event, IncomingPhoneNo, OtpCode


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('email',)
    list_filter = ('is_submitted',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'country_code',
                  'phone', 'city', 'country', 'project_url',
                  'issue_desc', 'project_info', 'project_impact',
                  'contribution_url', 'feedback', 'expertise',
                  'interest', 'team', 'profile_url', 'hackathon', 'is_email_verified',
                   'is_phone_verified', 'is_submitted', 'coder_password')}),
        ('Permissions', {'fields': ('is_staff', 'is_admin', 'is_superuser' ,'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_submitted')}
        ),
    )
    search_fields = ['is_submitted']
    ordering = ('is_submitted',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event)
admin.site.register(IncomingPhoneNo)
admin.site.register(OtpCode)
