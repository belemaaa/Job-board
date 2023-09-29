from django.urls import path
from . import views
from . import hirer_views as hv

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('signup/confirm/', views.CodeConfirmation.as_view()),
    path('login/', views.Login.as_view()),
    path('gigs/view/', views.ViewGigs.as_view()),
    path('gigs/search', views.SearchGigs.as_view()),
    path('gigs/view/<int:id>/', views.Gig_Detail.as_view()),
    path('posts/view/', views.Post.as_view()),
    #freelancer
    path('freelancer_profile/create/', views.FreelancerProfile.as_view()),
    path('freelancer_profile/<int:user_id>/view/', views.FreelancerProfile.as_view()),
    path('posts/create/', views.Post.as_view()),
    path('posts/<int:id>/delete/', views.Post.as_view()),
    path('gigs/save/<int:gig_id>/', views.Save_Gig.as_view()),
    path('gigs/collection/', views.Save_Gig.as_view()),
    path('gigs/bid/<int:gig_id>/', views.Bid.as_view()),
    #hirer
    path('hirer_profile/create/', hv.HirerProfile.as_view()),
    path('hirer_profile/<int:user_id>/view/', hv.HirerProfile.as_view()),
    path('gigs/create/', hv.Gig.as_view()),
    path('gigs/update/<int:gig_id>/', hv.Gig.as_view()),
    path('gigs/delete/<int:gig_id>/', hv.Gig.as_view()),
    path('gigs/personal/<int:id>/', hv.Hirer_Gigs_Single.as_view())
]