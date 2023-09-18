from django.urls import path
from . import views
from . import hirer_views as hv

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('gigs/view/', views.ViewGigs.as_view()),
    path('gigs/search/', views.SearchGigs.as_view()),
    path('gigs/view/<int:id>/', views.Gig_Detail.as_view()),
    path('posts/view/', views.Post.as_view()),

    #freelancer
    path('freelancer_profile/create/', views.FreelancerProfile.as_view()),
    path('freelancer_profile/<int:user_id>/view/', views.FreelancerProfile.as_view()),
    path('posts/create/', views.Post.as_view()),
    path('posts/<int:id>/delete/', views.Post.as_view()),

    #hirer
    path('gigs/create/', hv.CreateGig.as_view()),
    path('gigs/personal/', hv.Hirer_Gigs.as_view())
]