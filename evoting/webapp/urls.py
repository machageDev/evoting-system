from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),  
    path('base', views.base, name="base"),
    path('login', views.user_login, name="login"), 
    path('register', views.register, name="register"),
    path('navbar', views.navbar, name="navbar"),
    path('dashboard',views.dashboard,name="dashboard"),
    


     #forgot passwor
    
    #manage elections

    
    path('create_election', views.create_election, name='create_election'),
    path('man_elections', views.manage_elections, name='man_elections'),
    path('edit_election', views.edit_election, name='edit_election'),
    path('delete_election', views.delete_election, name='delete_election'),

    


    path('forgot-password', views.send_otp, name='forgot_password'),
    path('verify-otp', views.otp, name='otp'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('send-otp', views.send_otp, name='send_otp'),  



     
    path('create-candidate', views.create_candidate, name='create_candidate'),
    path('edit-cand', views.edit_candidate, name='edit_cand'),
    path('delete-candidate', views.delete_candidate, name="delete_candidate"),
    path("manage-cand", views.manage_candidates, name="manage_candidates"),



     path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
     path('create_user', views.create_user,name='create_user'),
     path('edit_user', views.edit_user, name='edit_user'),
     path('man_users', views.man_users, name='man_users'),
  



    path("monitor/", views.monitor_voting, name="monitor_voting"),
    path("results", views.election_results, name="results"),
    path("voter_dashboard", views.voter_dashboard, name="voter_dashboard"),
    #path('vote/',views.voter,name="vote"),

    path("dashboard", views.voter_dashboard, name="voter_dashboard"),
    path("vote", views.vote, name="vote"),    
    path('results', views.view_result, name="view_result"),


 
    
    ]