from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + \
            ('email', 'bio', 'job_security_preference', 'expected_income')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['interests', 'strengths', 'weaknesses']
