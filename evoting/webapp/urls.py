from django.urls import path
from . import views
from .views import create_election, create_user, manage_elections, delete_election
from .views import send_otp, otp, reset_password  
from .views import monitor_voting, election_results


urlpatterns = [
    path('', views.home, name="index"),  
    path('base/', views.base, name="base"),
    path('login/', views.user_login, name="login"), 
    path('register/', views.register, name="register"),
    path('navbar/', views.navbar, name="navbar"),
    path('dashboard/',views.dashboard,name="dashboard"),


     #forgot password
    
    #manage elections

    path('create_election', create_election, name='create_election'),
    path('man_elections', manage_elections, name='man_elections'),
    


    path('forgot-password/', send_otp, name='forgot_password'),
    path('verify-otp/', otp, name='otp'),
    path('reset_password/', reset_password, name='reset_password'),

     
    path("create-candidate/", views.create_candidate, name="create_candidate"),
    path("edit-candidate/<int:candidate_id>/", views.edit_candidate, name="edit_candidate"),
    path("delete-candidate/<int:candidate_id>/", views.delete_candidate, name="delete_candidate"),
    path("manage-candidates/", views.manage_candidates, name="manage_candidates"),



     path('create-user/', create_user,name='create_user'),

    



    path("monitor/", monitor_voting, name="monitor_voting"),
    path("results/<int:election_id>/", election_results, name="results"),


]