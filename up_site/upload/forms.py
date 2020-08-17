from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['filename', 'image_original']


class ResizeImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['last_width', 'last_height']
