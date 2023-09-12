from django.shortcuts import render, redirect

from rest_framework.views import APIView

from .models import *
from .serializers import *

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')



class LoginAPIView(APIView):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        data = request.data 
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        return redirect('postlist-admin.html')

