#imports
from django import forms # django forms library
from django.contrib.auth.models import User # django user model
from django.core.exceptions import ValidationError # for email and password validation
from .models import UserProfile # custom model from models.py file

# user registration form
class UserRegistrationForm(forms.ModelForm):
	# custom input fields
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Re-Enter Password', widget=forms.PasswordInput)
	
	#email = forms.EmailField()

	# meta class
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email',)

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

# login form
class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

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
		