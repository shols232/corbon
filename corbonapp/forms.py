from django import forms
from .models import File, PrivateDocument
class FileForm(forms.ModelForm):
    """simple upload form."""

    class Meta:

        model = PrivateDocument
        fields = ('name','upload')
