from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),  
    path('base/', views.base, name="base"),
    path('login/', views.user_login, name="login"), 
    path('register/', views.register, name="register"),
    path('navbar/', views.navbar, name="navbar"),
    path('dashboard/',views.dashboard,name="dashboard"),


     #forgot password
    
    #manage elections

    path('create_election', views.create_election, name='create_election'),
    path('man_elections', views.manage_elections, name='man_elections'),
    


    path('forgot-password/', views.send_otp, name='forgot_password'),
    path('verify-otp/', views.otp, name='otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('send-otp/', views.send_otp, name='send_otp'),  



     
    path('create-candidate/<int:election_id>/', views.create_candidate, name='create_candidate'),
    path("edit-candidate/<int:candidate_id>/", views.edit_candidate, name="edit_candidate"),
    path("delete-candidate/<int:candidate_id>/", views.delete_candidate, name="delete_candidate"),
    path("manage-candidates/", views.manage_candidates, name="manage_candidates"),



     path('create-user/', views.create_user,name='create_user'),

    



    path("monitor/", views.monitor_voting, name="monitor_voting"),
    path("results/<int:election_id>/", views.election_results, name="results"),
    path("voter_dashboard/", views.voter_dashboard, name="voter_dashboard"),
    #path('vote/',views.voter,name="vote"),

    path("dashboard/", views.voter_dashboard, name="voter_dashboard"),
    path("vote/", views.vote, name="vote"),    
    path("results/<int:post_id>/", views.view_result, name="view_result"),


 
    
    ]