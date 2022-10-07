from django import forms
from .models import *

class NippoFormClass(forms.Form):
    title = forms.CharField()
    content = forms.CharField()


#以下、お試し用

#ブログ投稿フォーム
class PostForm(forms.Form):
    
    class Meta:
        model = Post
        fields = '__all__'
    
#ブログ　インラインフォームセット
Formset = forms.inlineformset_factory(
    Post, ContentsCard, fields='__all__',
    extra=1,  can_delete=True
)
