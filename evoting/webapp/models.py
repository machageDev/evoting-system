from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    username=models.CharField(max_length=100)
    age=models.CharField(max_length=18)



class Election(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
    ]

    name = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    from django.utils import timezone
    some_field = models.DateTimeField(default=timezone.now)  # Example for a DateTimeField

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name


class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='candidate_pics/', blank=True, null=True)  


class User(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone_number = models.CharField(max_length = 15, blank=True,null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):    
        return self.user.username 