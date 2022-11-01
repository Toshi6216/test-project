from django import forms
from .models import *
from django.forms.models import inlineformset_factory

class NippoFormClass(forms.Form):
    title = forms.CharField()
    content = forms.CharField()


#以下、お試し用

#ブログ投稿フォーム
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'
        
    
class ContentsCardForm(forms.ModelForm):  #コンテンツカードのフォーム追加
    class Meta:
        model = ContentsCard
        fields = '__all__'

#ブログ　インラインフォームセット
CardFormset = forms.inlineformset_factory(
    Post, ContentsCard, fields='__all__',
    form=ContentsCardForm,  #追加したフォームを渡す
    extra=1,  can_delete=False
)

