from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Post
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Frimpong'}),
            'username': forms.TextInput(attrs={'placeholder': 'frimpong'}),
            'email': forms.EmailInput(attrs={'placeholder': 'frimpong@email.com'}),
            'password1': forms.PasswordInput(attrs={'placeholder': '********'}),
            'password2': forms.PasswordInput(attrs={'placeholder': '********'}),
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'avatar', 'cover_image']


class PostFeedForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['host', 'no_of_likes']
