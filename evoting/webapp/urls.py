from django.urls import path
from . import views
from . views import LoginVoter, user_profile
from django.contrib.auth.views import LogoutView
from django.conf.urls import handler404
from .views import custom_404_view

handler404 = custom_404_view
  # webapp/urls.py
from .views import VoteList 
from .views import RegisterVoter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ElectionViewSet, PostViewSet, CandidateViewSet

router = DefaultRouter()
router.register(r'elections', ElectionViewSet)
router.register(r'posts', PostViewSet)
router.register(r'candidates', CandidateViewSet)




     # This includes the generated URL paths for your API views


urlpatterns = [
    
    path('api/', include(router.urls)), 
    path('', views.home, name='home'),  
    path('base', views.base, name='base'),
    path('login', views.user_login, name="login"), 
    path('register', views.register, name="register"),
    path('navbar', views.navbar, name="navbar"),
    path('dashboard',views.dashboard,name="dashboard"),
    
    path('logout', LogoutView.as_view(), name='logout'),

    


    
    
    #manage elections    
    path('create_election', views.create_election, name='create_election'),
    path('man_elections', views.manage_elections, name='man_elections'),
    path('edit_election', views.edit_election, name='edit_election'),
    path('delete_election', views.delete_election, name='delete_election'),
  
    


    path('forgot-password', views.send_otp, name='forgot_password'),
    path('verify-otp', views.otp, name='otp'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('send-otp', views.send_otp, name='send_otp'),  



     
    path('create_candidate', views.create_candidate, name='create_candidate'),
    path('edit_cand', views.edit_candidate, name='edit_cand'),
    path('delete_cand', views.delete_candidate, name='delete_cand'),
    path("manage_cand", views.manage_candidates, name='manage_cand'),
    path('save_changes', views.save_changes, name='save_changes'),


    path('delete_user', views.delete_user, name='delete_user'),
    path('create_user', views.create_user,name='create_user'),
    path('edit_user', views.edit_user, name='edit_user'),
    path('man_users', views.man_users, name='man_users'),
    path('save_changes', views.save_changes, name='save_changes'),
  


    path('result', views.result, name='result'),
    path('monitor', views.monitor_voting, name='monitor_voting'),
    path("voter_dashboard", views.voter_dashboard, name='voter_dashboard'),
    path('vote',views.vote,name="vote"),
    path('submit_vote', views.submit_vote, name='submit_vote'),

     

    

    path('profile', views.profile, name='profile'),
    path('edit_profile',views.edit_profile, name = "edit_profile"),      
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),

   


    path('api/votes/', VoteList.as_view(), name='vote-list'),  # Define the API endpoint    # webapp/urls.py

    path('api/register/', RegisterVoter.as_view(), name='register'),
    path('api/login/', LoginVoter.as_view(), name='login'),
   

    
    ]
