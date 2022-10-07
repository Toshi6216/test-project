from django import forms
from .models import *

class PostForm(forms.Form):
    
    title = forms.CharField(max_length=30, label='タイトル')
    
    
Formset = forms.inlineformset_factory(
    Post, ContentsCard, fields='__all__',
    extra=1,  can_delete=True
)

class NippoFormClass(forms.Form):
    title = forms.CharField()
    content = forms.CharField()