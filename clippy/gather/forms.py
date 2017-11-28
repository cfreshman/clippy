from django import forms
    
class SearchForm(forms.Form):
    username = forms.CharField()
    
class GroupForm(forms.Form):
    event_name = forms.CharField(label="Group Name")
    description = forms.CharField(label="Group Description")
    group_image = forms.ImageField(label="Group Image")
    Members = forms.CharField(label="Members")
