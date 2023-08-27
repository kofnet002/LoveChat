from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Post
from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth import authenticate



class MyUserCreationForm(UserCreationForm):
    # adding email to the built in UserCreationForm
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

        image = CloudinaryFileField(label="avatar",options={'folder' : 'Profiles/'}, required=False)
        image = CloudinaryFileField(label="cover_image",options={'folder' : 'Profiles/',}, required=False)
        
        # cleaning user inputs
        def clean_email(self):
            email = self.cleaned_data['email'].lower()
            try:
                account = User.objects.get(email=email)
            except Exception as e:
                return email
            raise forms.ValidationError(f'Email {email} is already in use!')

        def clean_username(self):
            username = self.cleaned_data['username']
            try:
                account = User.objects.get(username=username)
            except Exception as e:
                return username
            raise forms.ValidationError(f'Username {username} is already in use!')


class UserAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username', 'password')

	def clean(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if not authenticate(username=username, password=password):
				raise forms.ValidationError("Invalid Credentials!")
               

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'avatar', 'cover_image']


class PostFeedForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['host', 'no_of_likes']
        image = CloudinaryFileField(options={'folder' : 'Posts/'})
