from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Election, Candidate, Vote, Voter, Post

User = get_user_model()

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Voter
        fields = ['name', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', None)
        )
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")


# Election Serializer
class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['id', 'name', 'date', 'status']


# Candidate Serializer
class CandidateSerializer(serializers.ModelSerializer):
    election = ElectionSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'position', 'election', 'profile_picture']


# Vote Serializer
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['candidate']

    def create(self, validated_data):
        user = self.context['request'].user
        vote = Vote.objects.create(user=user, **validated_data)
        return vote


# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'name']
