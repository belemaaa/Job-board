from django.shortcuts import render
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.views import APIView
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.authtoken.models import Token
import secrets
from django.core.mail import send_mail
from functools import reduce
from operator import or_
from django.db.models import Q

class Signup(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            raw_password = serializer.validated_data.get('password')
            hashed_password = make_password(raw_password)
            
            user_exists = models.User.objects.filter(username=username)
            if user_exists:
                return Response({'error': 'user with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            # send mail...
            serializer.save(password = hashed_password)
            return Response({'message': 'signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Login(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            try:
                user = models.User.objects.get(username=username)
            except models.User.DoesNotExist:
                user=None
            if user is not None and check_password(password, user.password):
                token = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'login successful',
                    'access_token': token.key,
                    'user_id': user.id
                }, status=status.HTTP_200_OK)
            return Response({'error': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchJobs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        search_query = self.request.query_params.get('q', None)
        queryset = models.Job.objects.all()
        if search_query:
            queryset = queryset.filter(
                Q(job_name__icontains=search_query) |
                Q(job_owner__icontains=search_query)
            )
        serializer = serializers.JobSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)