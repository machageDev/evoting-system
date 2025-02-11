from django.urls import path
from . import views
from .views import create_election, manage_elections, delete_election
from .views import send_otp, otp, reset_password  


urlpatterns = [
    path('', views.home, name="index"),  
    path('base/', views.base, name="base"),
    path('login/', views.user_login, name="login"), 
    path('register/', views.register, name="register"),
    path('navbar/', views.navbar, name="navbar"),
    path('dashboard/',views.dashboard,name="dashboard"),

     #forgot password
    
    #manage eections

    path('create/', create_election, name='create_election'),
    path('manage/', manage_elections, name='manage_elections'),


    path('forgot-password/', send_otp, name='forgot_password'),
    path('verify-otp/', otp, name='otp'),
    path('reset_password/', reset_password, name='reset_password'),


]
