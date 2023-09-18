from django.urls import path, include 
from django.contrib.auth import views as auth_views
from . import views 

app_name = 'blog'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    # path('login/', auth_views.LoginView.as_view(template_name='blog_app/login.html'), name='login'),
    path('login/',views.login_Form,name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('',views.post_list,name='post_list'),
    path('board/<int:post_id>/',views.post_detail,name='board'),
    path('write/', views.write, name='write'),
    path('edit/<int:post_id>/', views.write, name='write'),
    path('image_upload', views.image_upload.as_view(), name='image_upload'),
    path('post_list/<str:category>/', views.filtered_post_list, name='filtered_post_list'),
]
