from distutils.command.build_scripts import first_line_re
from django import forms

class TestblogFormClass(forms.Form):
    title = forms.CharField(label='タイトル', max_length=100)
    content = forms.CharField(label='内容', max_length=1000)

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        super().__init__(*args, **kwargs)
