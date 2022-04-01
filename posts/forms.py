# imports
from django import forms
from django.forms import TextInput, EmailInput, Textarea
from .models import Post


# to create new posts
class NewPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'body', 'topics', 'post_image')
		widgets = {'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Title'
                }),
				'body': Textarea(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Body'
				}),
				'topics': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Tags'
				})
		}


# to edit old posts
class EditPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'body', 'topics', 'post_image')
		widgets = {'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Title'
                }),
				'body': Textarea(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Body'
				}),
				'topics': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Tags'
				})
		}

