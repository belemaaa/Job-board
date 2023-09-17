from django.urls import path
from . import views
import hirer_views as hv

url_patterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('view_gigs/', views.ViewGigs.as_view()),
    path('search_gig/', views.SearchGigs.as_view()),
    path('gig/<int:id>', views.SearchGigs.as_view()),

    #freelancer
    path('freelancer_profile', views.FreelancerProfile.as_view()),

    #hirer
    path('create_gig/', hv.CreateGig.as_view()),
    path('personal_gigs/', hv.Hirer_Gigs.as_view())
]