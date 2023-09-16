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
    class Meta:
        model = models.Gig
        fields = ['gig_owner', 'gig_name', 'gig_description']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = ['job_owner', 'job_name', 'job_description', 'job_requirements']