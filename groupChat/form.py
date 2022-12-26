from django.forms import ModelForm
from django import forms
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Django, ReactJS, Spring Boot...'}),
            'description': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }
