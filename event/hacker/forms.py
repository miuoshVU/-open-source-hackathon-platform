from default.models import CustomUser, OtpCode
from django import forms
from default.forms import CustomUserChangeForm
from .models import HackerInfo


class CustomHackerChangeForm(CustomUserChangeForm):
    class Meta:
        model = HackerInfo
        fields = ()

        widgets = {

        }


class PhoneVerificationForm(forms.ModelForm):
    class Meta:
        model = OtpCode
        fields = ('otpcode',)

class ChangePhoneForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('country_code', 'phone',)
        widget = {
             'country_code': forms.Select(attrs={'class': 'form-select bg-cream'}),
             'phone': forms.TextInput(attrs={'class': 'form-control bg-cream', 'type': "tel", 'placeholder': '7861234567'}),
        }
                    


