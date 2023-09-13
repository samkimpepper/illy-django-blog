from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from .forms import CustomLoginForm

from rest_framework import generics


from rest_framework.views import APIView

from .models import *
from .serializers import *


class RegisterAPIView(APIView):
    def get(self, request):
        return render(request, 'blog/register.html')
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return redirect('login')

class LoginAPIView(APIView):
    def get(self, request):
        return render(request, 'blog/login.html')
    def post(self, request):
        data = request.data 
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        return redirect('blog/postlist-admin.html')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('blog_app:post_list')
    else:
        form = CustomLoginForm(data=request.POST or None)  # 커스텀 로그인 폼 사용
        if request.method == "POST":

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('blog_app:post_list')  # 슈퍼유저와 일반 사용자 모두 동일한 페이지로 리다이렉션
        return render(request, 'blog/login.html', {'form': form})
