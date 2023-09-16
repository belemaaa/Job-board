from django.shortcuts import render
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.views import APIView
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from functools import reduce
from operator import or_
from django.db.models import Q


class FreelancerProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.FreelancerSerializer(data=request.data)
        if serializer.is_valid():
            field = serializer.validated_data.get('field')
            qualifications = serializer.validated_data.get('qualifications')

            serializer.save(user=request.user)
            return Response({'message': 'freelancer has been created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewGigs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        gigs_list = models.Gig.objects.all()
        serializer = serializers.GigSerializer(gigs_list, many=True)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class Gig_Detail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        queryset = models.Gig.objects.get(id=id)
        serializer = serializers.GigSerializer(queryset, many=False)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)