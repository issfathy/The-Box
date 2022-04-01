#imports
from django import forms # django forms library
from django.forms import TextInput, EmailInput, Textarea
from django.contrib.auth.models import User # django user model
from django.core.exceptions import ValidationError # for email and password validation
from .models import UserProfile # custom model from models.py file

# user registration form
class UserRegistrationForm(forms.ModelForm):
	# custom input fields
	password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'style': 'width: 300px;', 'class': 'form-control'}))
	password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Re-Enter Password', 'style': 'width: 300px;', 'class': 'form-control'}))
	
	#email = forms.EmailField()

	# meta class
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')
		widgets = {'username': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Username'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'}),
			'first_name': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'First Name'}),
			'last_name': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Last Name'})
		}

	# to check for password match
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match!')

		return cd['password2']

# profile registration form
class UserProfileForm(forms.ModelForm):
	# meta class
	class Meta:
		model = UserProfile
		fields = 'bio','profile_pic'
		widgets = {'bio': Textarea(attrs={
                'class': "form-control",
                'style': 'width: 20px;',
				'style': 'height: 100px;',
                'placeholder': ''
                })
		}

# login form
class LoginForm(forms.Form):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username', 'style': 'width: 300px;', 'class': 'form-control'}))
	password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'style': 'width: 300px;', 'class': 'form-control'}))

# edit profile form
class EditProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = '__all__'
		exclude = ['following', 'user']

class DeleteProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = '__all__'

class ThreadForm(forms.Form):
	username = forms.CharField(label='', max_length=100)
	
class MessageForm(forms.Form):
	message = forms.CharField(label='', max_length=1000)