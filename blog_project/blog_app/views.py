from django.shortcuts import render, redirect

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

