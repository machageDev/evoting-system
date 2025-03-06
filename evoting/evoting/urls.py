"""
URL configuration for evoting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  # Token refresh view
from webapp.views import CustomTokenObtainPairView 

from webapp.views import RegisterView, LoginView, CandidateViewSet, ElectionViewSet, PostViewSet, VoteViewSet, VoterViewSet

# Create a router instance and register viewsets
router = DefaultRouter()
router.register(r'elections', ElectionViewSet)
router.register(r'posts', PostViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'voters', VoterViewSet)
router.register(r'votes', VoteViewSet)

# Define urlpatterns
urlpatterns = [
    path('', include('webapp.urls')), 
    path('admin/', admin.site.urls),
    
    path('api/', include(router.urls)),    
    path('api-auth/', include('rest_framework.urls')),    
    path('api/token/', obtain_auth_token, name='api_token_auth'),    
    path('api/register/', RegisterView.as_view(), name='register'),    
    path('api/login/', LoginView.as_view(), name='login'),
    
    path('api/elections/', ElectionViewSet.as_view({'get': 'list'}), name='election-list'),
    path('api/candidates/', CandidateViewSet.as_view({'get': 'list'}), name='candidate-list'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Custom login endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
