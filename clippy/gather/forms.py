from django import forms
from django.forms import ModelForm
from .models import Profile

class SearchForm(forms.Form):
    username = forms.CharField()

class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name') 
    username = forms.CharField(label='Username')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'picture']
