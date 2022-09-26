from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    Picture_Type = (
        ("black_white", "白黒"),
        ("mosaic", "モザイク"),
    )
    picture_type = forms.ChoiceField(choices=Picture_Type, label='', widget=forms.RadioSelect)

    class Meta:
      model = Document
      fields = ('photo','picture_type')

# class DocumentForm(forms.Form):
#   photo = forms.ImageField(label="動画を選択")
#   class Meta:
#       model=Document
#       fields = ('photo',)

