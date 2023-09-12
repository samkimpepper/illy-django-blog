from django.urls import path, include 
from django.contrib.auth import views as auth_views
from . import views 

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
