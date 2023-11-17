from django import forms
from main.models import ImageInput, ImageDataset
from main.models import ImageDataset

class ImgInputForm(forms.ModelForm):
    class Meta:
        model = ImageInput
        fields = ('image',)
        
class DatasetForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),)
    class Meta:
        model = ImageDataset
        fields = ('image',)
        
        