from requests import Response
from rest_framework import serializers
from .models import Election, Candidate, Voter, Vote
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Voter  # Import your Voter model
from rest_framework import status
from .models import Post

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    # Do not include password handling in this serializer
    class Meta:
        model = Voter
        fields = ['user', 'name', 'phone_number', 'email']  # Only these fields

    def create(self, validated_data):
        # Create the User object without password handling
        user = User.objects.create(
            username=validated_data['user'],  # user as username
            email=validated_data['email']     # email for the user
        )

        # Create the Voter object and link it to the User
        voter = Voter.objects.create(
            user=user,  # Link user to the voter
            name=validated_data['name'],
            phone_number=validated_data.get('phone_number', '')  # Optional field
        )

        return voter

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        data["user"] = user
        return data
    
class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['id', 'name', 'date', 'created_at', 'status']



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'name']



class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'election', 'name', 'position', 'profile_picture']
