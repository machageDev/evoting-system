from django import forms
from .models import Election

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['name', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
