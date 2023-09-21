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
from cloudinary.uploader import upload
from django.core.mail import send_mail
from functools import reduce
from operator import or_
from django.db.models import Q
from .permissions import IsPostOwner
import random
from django.conf import settings
from django.shortcuts import get_object_or_404

cloudinary.config( 
  cloud_name = "drrnvvy3v", 
  api_key = "449689815376197", 
  api_secret =  "faWVEPjlcc0f6HtaxcG1kMJ-2xI"
)
class Signup(APIView):
    authentication_classes = []
    permission_classes = []
    def generate_code(self):
        return str(random.randint(100000, 999999))
    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            email = validated_data.get('email')
            user_exists = models.User.objects.filter(email=email)
            if user_exists:
                return Response({'error': 'user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            code = self.generate_code()
            confirmation_code = models.ConfirmationCode(email=email, code=code, user=validated_data)
            confirmation_code.save()
            # send verification code to user's email
            subject = 'Signup Verification Code'
            message = f"Hello {validated_data.get('first_name')} {validated_data.get('last_name')},\n\n"\
                      f"Your verification code is: {code}\n\n"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response({'message': f'Your verification has been sent to {email}', 'verification_code': code}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CodeConfirmation(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')
        confirmation_code = get_object_or_404(models.ConfirmationCode, email=email)
        if confirmation_code.is_verified:
            return Response({'error': 'Code has already been used'}, status=status.HTTP_400_BAD_REQUEST)
        elif confirmation_code.code == code and confirmation_code.user.email == email:
            hashed_password = make_password(confirmation_code.user.password)
            user = models.User(
                first_name=confirmation_code.user.first_name,
                last_name=confirmation_code.user.last_name,
                username=confirmation_code.user_details['username'],
                email=confirmation_code.user_details['email'],
                password=hashed_password
            )
            user.save()
            #mark the code as verified and delete it
            confirmation_code.is_verified = True
            confirmation_code.save()
            return Response({'message': 'Signup was successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)

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
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'login successful', 
                    'token': token.key, 
                    'user_id': user.id}, status=status.HTTP_200_OK)
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
            return Response({'message': 'freelancer has been created' if created else 'freelancer profile updated', 
                             'user': freelancer.user.id,
                             'profile_data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, user_id):
        try:
            freelancer_profile = models.Freelancer.objects.get(user=user_id)
        except models.Freelancer.DoesNotExist:
            return Response({'error': 'freelancer not found'}, status=status.HTTP_404_NOT_FOUND) 
        user = models.Freelancer.objects.get(user=self.request.user)
        freelancer_posts = models.Post.objects.filter(user=user)
        post_serializer = serializers.PostSerializer(freelancer_posts, many=True)

        profile_data = {
            'first_name': freelancer_profile.user.first_name,
            'last_name': freelancer_profile.user.last_name,
            'username': freelancer_profile.user.username,
            'email': freelancer_profile.user.email,
            'field': freelancer_profile.field,
            'qualifications': freelancer_profile.qualifications,
            'posts': post_serializer.data
        }
        return Response({'data': profile_data}, status=status.HTTP_200_OK)

class ViewGigs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        gig_list = models.Gig.objects.all()
        gigs_with_bids = []
        for gig in gig_list:
            bids = gig.bid_set.all()
            bid_count = bids.count()
            bidders = [bid.bidder.user.username for bid in bids]
            gig_serializer = serializers.GigSerializer(gig)  # serialize the gig object
            gig_data = {
                'gig': gig_serializer.data,
                'bid_count': bid_count,
                'bidders': bidders,
            }
            gigs_with_bids.append(gig_data)
        return Response(gigs_with_bids, status=status.HTTP_200_OK)

class SearchGigs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        search_query = self.request.query_params.get('q', None)
        queryset = models.Gig.objects.all()
        if search_query:
            search_parts = search_query.split()
            if len(search_parts) == 2:
                role, role = search_parts
                queryset = queryset.filter(Q(role__icontains=role) & (Q(role__icontains=role)))
            elif len(search_parts) == 1:
                query_parts = [Q(user__user__username__icontains=part) | Q(role__icontains=part) | Q(gig_description__icontains=part) | 
                               Q(user__user__first_name__icontains=part) | Q(user__user__last_name=part) for part in search_parts]
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
    
class Post(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPostOwner]
    def post(self, request):
        serializer = serializers.PostSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = ''
            # retrieve the Freelancer instance associated with the authenticated user
            user = models.Freelancer.objects.get(user=self.request.user)
            image = request.data.get('image')
            if image:
                uploaded_image = upload(image)
                serializer.validated_data['image'] = uploaded_image['secure_url']
            serializer.save(user=user)
            return Response({'message': 'post creation successful', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def get(self, request):
        qs = models.Post.objects.all()
        serializer = serializers.PostSerializer(qs, many=True)
        return Response({'posts': serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        try:
            user = models.Freelancer.objects.get(user=self.request.user)
            post = models.Post.objects.get(id=id, user=user)
            self.check_object_permissions(request, post)
            post.delete()
            return Response({'message': 'post has been deleted'}, status=status.HTTP_200_OK)
        except models.Post.DoesNotExist:
            return Response({'error': 'post not found'}, status=status.HTTP_404_NOT_FOUND)

class Get_Single_Freelancer_Posts(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, user_id):
        freelancer = models.Freelancer.objects.get(user=user_id)
        queryset = models.Post.objects.filter(user=freelancer)
        serializer = serializers.PostSerializer(queryset, many=True)
        return Response({'posts': serializer.data}, status=status.HTTP_200_OK)

class Bid(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, gig_id):
        try:
            gig = models.Gig.objects.get(id=gig_id)
        except models.Gig.DoesNotExist:
            return Response({'error': f'gig with id {gig_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        bidder = models.Freelancer.objects.get(user=self.request.user)
        serializer = serializers.BidSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data.get('message') or None
            if message is None:
                message = 'New bid alert.'
            if gig.user == bidder:
                return Response({'error': 'You cannot bid your own gig'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(gig=gig, bidder=bidder, message=message)
            return Response({'message': f'New bid created for gig {gig_id}'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# limited to only freelancer users   
class Save_Gig(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, gig_id):
        try:
            # retrieve freelancer object associated with the logged in user (if freelancer)
            user = models.Freelancer.objects.get(user=self.request.user)
            gig = models.Gig.objects.get(id=gig_id)
        except models.Gig.DoesNotExist:
            return Response({'error': 'gig not found'}, status=status.HTTP_404_NOT_FOUND) 
        saved_gig, created = models.SavedGig.objects.get_or_create(user=user, gig=gig)
        if created:
            return Response({'message': 'gig saved successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'gig is already saved to your collection.'}, status=status.HTTP_200_OK)    
    # retrieve saved gigs
    def get(self, request):
        user = models.Freelancer.objects.get(user=self.request.user)
        saved_gigs = models.SavedGig.objects.get(user=user)
        serializer = serializers.SavedGigSerializer(saved_gigs, many=True)
        if saved_gigs is None:
            return Response({'message': 'No gig has been saved'},status=status.HTTP_200_OK)
        else:
            gig = {
                "owner": {
                    "first_name": saved_gigs.gig.user.user.first_name,
                    "last_name": saved_gigs.gig.user.user.last_name,
                    "username": saved_gigs.gig.user.user.username,
                    "email": saved_gigs.gig.user.user.email,
                },
                "gig": {
                    "role": saved_gigs.gig.role,
                    "gig_description": saved_gigs.gig.gig_description,
                    "gig_requirements": saved_gigs.gig.gig_requirements
                }
            }
            return Response(gig, status=status.HTTP_200_OK)

