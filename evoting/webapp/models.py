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
    
# Custom Manager for Voter
class VoterManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

# Custom Voter model extending AbstractUser
class Voter(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=254)

    user = models.ForeignKey(User,on_delete=models.CASCADE,default = None)
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