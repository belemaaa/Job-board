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
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.mail import send_mail
from functools import reduce
from operator import or_
from django.db.models import Q

cloudinary.config( 
  cloud_name = "drrnvvy3v", 
  api_key = "449689815376197", 
  api_secret =  "faWVEPjlcc0f6HtaxcG1kMJ-2xI"
)

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

class FreelancerProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.FreelancerSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            freelancer, created = models.Freelancer.objects.get_or_create(user=user)

            freelancer.field = serializer.validated_data.get('field')
            freelancer.qualifications = serializer.validated_data.get('qualifications')
            freelancer.save()

            return Response({'message': 'freelancer has been created' if created else 'freelancer profile updated'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewGigs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        gigs_list = models.Gig.objects.all()
        serializer = serializers.GigSerializer(gigs_list, many=True)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class SearchGigs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        search_query = self.request.query_params.get('q', None)
        queryset = models.Gig.objects.all()
        if search_query:
            search_parts = search_query.split()

            if len(search_parts) == 2:
                role = search_parts
                queryset = queryset.filter(Q(role__icontains=role))
            elif len(search_parts == 1):
                query_parts = [Q(user__icontains=part) | Q(role__icontains=part) | Q(gig_description__icontains=part) for part in search_parts]
                combined_query = reduce(or_, query_parts)
                queryset = queryset.filter(combined_query)
            else:
                return Response({'message': 'can only enter two search parameters'})
        serializer = serializers.GigSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class Gig_Detail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        queryset = models.Gig.objects.get(id=id)
        serializer = serializers.GigSerializer(queryset, many=False)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)