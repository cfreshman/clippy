from django import forms
    
class SearchForm(forms.Form):
    username = forms.CharField()
