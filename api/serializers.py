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
        fields = ['owner_id', 'gig_name', 'gig_description']
    
    def get_owner_id(self, obj):
        return obj.id
