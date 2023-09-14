from django.urls import path, include 
from django.contrib.auth import views as auth_views
from . import views 

app_name = 'blog'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    # path('login/', auth_views.LoginView.as_view(template_name='blog_app/login.html'), name='login'),
    path('login/',views.login_Form,name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('board_client',views.board_client,name='board_client'),
    path('board_admin',views.board_admin,name='board_client')
]