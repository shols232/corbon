from django import forms
from .models import Files, PrivateDocument
class FileForm(forms.ModelForm):
    """simple upload form."""

    class Meta:

        model = PrivateDocument
        fields = ('name','upload')


class CreateUsersForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file', )
