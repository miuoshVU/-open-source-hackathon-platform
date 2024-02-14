from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from hacker.models import HackerInfo


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control bg-cream', 'onblur': 'passwordValidation()'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
        attrs={'class': 'form-control bg-cream',  'onblur': 'password2Validation()'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'country_code',
                  'phone'
                  )

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-cream', 'placeholder': 'Jane', 'name': 'fname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-cream', 'placeholder': 'Doe', 'name': 'lname'}),
            'email': forms.TextInput(attrs={'class': 'form-control bg-cream', 'placeholder': 'Jdoe123@gmail.com', 'type': 'email', 'onblur': 'emailValidation()', "pattern": "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$", "title": "username@domain.tld"}),
            'country_code': forms.Select(attrs={'class': 'form-select bg-cream'}),
            'phone': forms.TextInput(attrs={'class': 'form-control bg-cream', 'type': "tel", 'placeholder': '7861234567'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class HackerCreationForm(forms.ModelForm):

    class Meta:
        model = HackerInfo
        fields = ()

        widgets = {
        }


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'city', 'country', 'project_url',
                  'issue_desc', 'project_info', 'project_impact',
                  'contribution_url', 'feedback', 'expertise',
                  'interest', 'team', 'profile_url', 'hackathon', 'is_submitted')

        widgets = {
            # Personal data
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-cream', 'placeholder': 'Jane'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-cream', 'placeholder': 'Doe'}),
            'email': forms.TextInput(attrs={'class': 'form-control bg-cream', 'readonly': True, 'type': 'email', 'placeholder': 'Jdoe123@gmail.com', "pattern": "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$", "title": "username@domain.tld"}),
            'country_code': forms.Select(attrs={'class': 'form-select bg-cream'}),
            'phone': forms.TextInput(attrs={'class': 'form-control bg-cream', 'readonly': True, 'type': "tel", 'placeholder': '7861234567'}),
            'city': forms.TextInput(attrs={'class': 'form-control bg-cream'}),
            'country': forms.Select(attrs={'class': 'form-select bg-cream'}),
            # Challenge questions
            'project_url': forms.TextInput(attrs={'class': 'form-control bg-cream', 'placeholder': 'Please provide the URL to the original project.'}),
            'issue_desc': forms.Textarea(attrs={'class': 'form-control bg-cream', 'placeholder': 'Describe the issue/enhancement/challenge/problem you worked on. You can add an applicable link for reference. (max 1500 words)'}),
            'project_info': forms.Textarea(attrs={'class': 'form-control bg-cream', 'placeholder': 'Tell us about your work and the contribution you made. (E.g.: what you have done to enhance or solve the issue/challenge/problem) (max 1500 words)'}),
            'project_impact': forms.Textarea(attrs={'class': 'form-control bg-cream', 'placeholder': 'How do you think the your work will effect others? Please explain what you anticipate as the impact of your work on the works and lives of others that will benefit from it. (max 1000 words)'}),
            'contribution_url': forms.TextInput(attrs={'class': 'form-control bg-cream', 'placeholder': 'Please provide the URL to your work. (E.g.: Link to a patch file or git commit in a public repository)'}),
            # Optional
            'feedback': forms.Textarea(attrs={'class': 'form-control bg-cream', 'placeholder': 'Is there anything else you would like to share? (max 1000 words)'}),
            'expertise': forms.Textarea(attrs={'class': 'form-control bg-cream', 'placeholder': 'What are your areas of expertise?'}),
            'interest': forms.Textarea(attrs={'class': 'form-control bg-cream', 'placeholder': 'What are your areas of interest?'}),
            'team': forms.Textarea(attrs={'class': 'form-control bg-cream', 'placeholder': 'If participating as a team, what is the name of your team? What is the role of each team member?'}),
            'profile_url': forms.TextInput(attrs={'class': 'form-control bg-cream', 'placeholder': 'What is the link to your github/gitlab profile?'}),
            'hackathon': forms.Textarea(attrs={'class': 'form-control bg-cream', 'placeholder': 'How did you hear about this hackathon?'}),

        }