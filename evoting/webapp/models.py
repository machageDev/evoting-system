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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):    
        return self.user.username 

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)  
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name} in {self.candidate.election.name}"
