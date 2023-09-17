from rest_framework import serializers
from . import models

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirmation_code']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField()


class GigSerializer(serializers.ModelSerializer):
    owner_id = serializers.SerializerMethodField()
    class Meta:
        model = models.Gig
        fields = ['owner_id', 'role', 'gig_description', 'gig_requirements', 'created_at']
    
    def get_owner_id(self, obj):
        return obj.id

class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Freelancer
        fields = ['user', 'field', 'qualifications']

class HirerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hirer
        fields = ['user', 'about']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['user', 'content', 'image', 'created_at']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bid
        fields = ['gig', 'bidder', 'message', 'created_at']