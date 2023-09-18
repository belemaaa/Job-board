from rest_framework import serializers
from . import models

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

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
        fields = ['field', 'qualifications']

class HirerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hirer
        fields = ['user', 'about']

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = models.Post
        fields = ['id', 'owner', 'content', 'image', 'created_at']

    def get_owner(self, obj):
        return {
            'first_name': obj.user.user.first_name,
            'last_name': obj.user.user.last_name,
            'username': obj.user.user.username,
            'email': obj.user.user.email,
            'field': obj.user.field
        }

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bid
        fields = ['gig', 'bidder', 'message', 'created_at']