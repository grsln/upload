from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['filename', 'image_original']
    #
    # def clean(self):
    #     number = self.cleaned_data['image_original']
    #     self.cleaned_data['full_number'] = code + number
# class ImageForm(forms.Form):
#     filename = forms.CharField(max_length=100)
#     image_url = forms.URLInput()
#     image_original = forms.ImageField()

# class MyForm(forms.Form):
#     even_field = forms.IntegerField(validators=[validate_even])