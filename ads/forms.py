from django import forms
from .models import Ad

class CreateAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["category", "title", "description", "condition"]
