from django import forms
from .models import File
class FileForm(forms.ModelForm):
    """simple upload form."""

    class Meta:

        model = File
        fields = ('name','zip_file')
