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



from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


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

    
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        


class ElectionFilterForm(forms.Form):
    """Form to filter elections."""
    status_choices = [("pending", "Pending"), ("active", "Active")]
    status = forms.ChoiceField(choices=status_choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    


from django.apps import apps

Election = apps.get_model('webapp', 'Election')
Voter = apps.get_model('webapp', 'Voter')




class VoterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['phone_number', 'otp_verified', 'status']
        widgets = {
            'status': forms.Select(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
        }
