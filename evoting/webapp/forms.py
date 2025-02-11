from django import forms
from .models import Election


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['name', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# forms.py


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

# forms.py

from .models import Candidate  # Assuming you have a Candidate model

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'position', 'profile_picture']

    position = forms.ChoiceField(
        choices=[
            ('chairperson', 'Chairperson'),
            ('vice_chairperson', 'Vice Chairperson'),
            ('treasurer', 'Treasurer'),
            ('secretary', 'Secretary'),
            ('member', 'Member'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    
