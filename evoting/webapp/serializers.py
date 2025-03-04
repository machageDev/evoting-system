from rest_framework import serializers, viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model, authenticate
from .models import Election, Post, Candidate, Vote, Voter
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Voter  
        fields = ['name', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Check if username already exists
        if Voter.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        user = Voter.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', None)
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    election = ElectionSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'position', 'election', 'profile_picture']

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email', 'phone_number']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['candidate']

    def create(self, validated_data):
        user = self.context['request'].user
        vote = Vote.objects.create(user=user, **validated_data)
        return vote
