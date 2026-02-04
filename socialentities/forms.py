from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SocialEntity

class SocialEntityCreationForm(UserCreationForm):
    class Meta:
        model = SocialEntity
        # Removemos 'username' e garantimos que o email seja usado
        fields = ('email',)

class SocialEntityChangeForm(UserChangeForm):
    class Meta:
        model = SocialEntity
        fields = '__all__'