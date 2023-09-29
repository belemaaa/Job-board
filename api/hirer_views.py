from django.shortcuts import render
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.views import APIView
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class HirerProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.HirerSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            hirer, created = models.Hirer.objects.get_or_create(user=user)
            hirer.about = serializer.validated_data.get('about')
            hirer.save()
            return Response({'message': 'hirer has been created' if created else 'hirer profile updated', 
                             'user': hirer.user.id,
                             'profile_data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, user_id):
        try:
            hirer_profile = models.Hirer.objects.get(user=user_id)
        except models.Hirer.DoesNotExist:
            return Response({'error': 'hirer not found'}, status=status.HTTP_404_NOT_FOUND) 
        user = models.Hirer.objects.get(user=self.request.user)
        gig_list = models.Gig.objects.all()
        gigs_with_bids = []
        for gig in gig_list:
            bids = gig.bid_set.all()
            bid_count = bids.count()
            bidders = [bid.bidder.user.username for bid in bids]
            gig_serializer = serializers.GigSerializer(gig)
            gig_data = {
                'gig': gig_serializer.data,
                'bid_count': bid_count,
                'bidders': bidders,
            }
            gigs_with_bids.append(gig_data)
        profile_data = {
            'first_name': hirer_profile.user.first_name,
            'last_name': hirer_profile.user.last_name,
            'username': hirer_profile.user.username,
            'email': hirer_profile.user.email,
            'about': hirer_profile.about,
            'gigs': gigs_with_bids
        }
        return Response({'data': profile_data}, status=status.HTTP_200_OK)

class Gig(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.GigSerializer(data=request.data)
        if serializer.is_valid():
            role = serializer.validated_data.get('role')
            gig_description = serializer.validated_data.get('gig_description')
            gig_requirements = serializer.validated_data.get('gig_requirements')
            # retrieve hirer instance 
            user = models.Hirer.objects.get(user=self.request.user)
            serializer.save(user=user)
            return Response({'message': 'Gig created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, gig_id):
        try:
            user = models.Hirer.objects.get(user=self.request.user)
            gig = models.Gig.objects.get(id=gig_id, user=user)
            serializer = serializers.GigSerializer(gig, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'gig data has been updated', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Gig.DoesNotExist:
            return Response({'error': 'gig not found.'}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, gig_id):
        try:
            user = models.Hirer.objects.get(user=self.request.user)
            instance = models.Gig.objects.get(id=gig_id, user=user)
            instance.delete()
            return Response({'message': 'gig has been deleted'}, status=status.HTTP_200_OK)
        except models.Gig.DoesNotExist:
            return Response({'error': 'gig not found'}, status=status.HTTP_404_NOT_FOUND)

# class Hirer_Gigs_Single(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, id):
#         try:
#             hirer = models.Hirer.objects.get(user=id)
#             # queryset = models.Gig.objects.filter(user=hirer)
#             gig_list = models.Gig.objects.filter(user=hirer)
#             gigs_with_bids = []
#             for gig in gig_list:
#                 bids = gig.bid_set.all()
#                 for bid in bids:
#                     bid_count = bids.count()
#                     bidder = bid.bidder.user.username
#                     bid_message = bid.message
#                     gig_serializer = serializers.GigSerializer(gig)
#                     gig_data = {
#                         'gig': gig_serializer.data,
#                         'bid_count': bid_count,
#                         'bidder': bidder,
#                         'bid_messages': bid_message
#                     }
#                     gigs_with_bids.append(gig_data)
#                     return Response(gigs_with_bids, status=status.HTTP_200_OK)
#         except models.Hirer.DoesNotExist:
#             return Response({'error': 'Hirer instance not found'}, status=status.HTTP_404_NOT_FOUND)

class Hirer_Gigs_Single(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            hirer = models.Hirer.objects.get(user=id)
        except models.Hirer.DoesNotExist:
            return Response({'error': 'Hirer instance not found'}, status=status.HTTP_404_NOT_FOUND)
        gig_list = models.Gig.objects.filter(user=hirer)
        gigs_with_bids = []
        for gig in gig_list:
            bids = gig.bid_set.all()
            bid_count = bids.count()
            bid_messages = []
            for bid in bids:
                bid_messages.append({
                    'freelancer': bid.bidder.user.username,
                    'message': bid.message
                })         
            gig_serializer = serializers.GigSerializer(gig)
            gig_data = {
                'gig_details': gig_serializer.data,
                'bid_count': bid_count,
                'bid_messages': bid_messages,
            }
            gigs_with_bids.append(gig_data)
        return Response(gigs_with_bids, status=status.HTTP_200_OK)
    
