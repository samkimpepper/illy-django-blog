from django.urls import path, include 
from django.contrib.auth import views as auth_views
from . import views 



urlpatterns = [
    path('login/', views.login, name='login_view', methods=['get']),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]