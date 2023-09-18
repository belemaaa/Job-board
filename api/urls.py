from django.urls import path
from . import views
from . import hirer_views as hv

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('view_gigs/', views.ViewGigs.as_view()),
    path('search_gig/', views.SearchGigs.as_view()),
    path('gig/<int:id>', views.ViewGigs.as_view()),

    #freelancer
    path('freelancer_profile/create/', views.FreelancerProfile.as_view()),
    path('freelancer_profile/<int:id>/view/', views.FreelancerProfile.as_view()),

    #hirer
    path('create_gig/', hv.CreateGig.as_view()),
    path('personal_gigs/', hv.Hirer_Gigs.as_view())
]