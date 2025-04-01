from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class Election(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
    ]

    name = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=255, default="unknown")
    profile_picture = models.ImageField(upload_to='candidate_pics/', blank=True, null=True)  

    def __str__(self):
        return f"{self.name} - {self.position}"
    
class Voter(models.Model):
    username = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=254)
    
    # ForeignKey to Django's built-in User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)  
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        candidate_name = self.candidate.name if self.candidate else "Unknown Candidate"
        election_name = self.candidate.election.name if self.candidate and self.candidate.election else "Unknown Election"
        return f"{self.user.username} voted for {candidate_name} in {election_name}"