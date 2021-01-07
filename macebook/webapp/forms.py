from django import forms
from .models import Picture


class PictureForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Picture
        fields = ('profilefield',)