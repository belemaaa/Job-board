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
    
class CreateGig(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.GigSerializer(data=request.data)
        if serializer.is_valid():
            role = serializer.validated_data.get('gig_name')
            gig_description = serializer.validated_data.get('gig_description')
            gig_requirements = serializer.validated_data.get('gig_requirements')

            serializer.save(user=request.user)
            return Response({'message': 'Gig created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Hirer_Gigs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        queryset = models.Gig.objects.filter(user=user)
        serializer = serializers.GigSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
     
    def put(self, request, gig_id):
        try:
            instance = models.Gig.objects.get(id=gig_id)
            serializer = serializers.GigSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Gig has been updated.', 'data': serializer.data}, status=status.HTTP_200_OK)
        except models.Gig.DoesNotExist:
            return Response({'error': 'Gig not found'}, status=status.HTTP_404_NOT_FOUND)

class GetAllGigs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        gigs_list = models.Gig.objects.all()
        serializer = serializers.GigSerializer(gigs_list, many=True)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
