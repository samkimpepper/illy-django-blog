from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .forms import LoginForm
from django.contrib.auth import authenticate, login

class RegisterAPIView(APIView):
    def get(self, request):
        return render(request, 'blog/register.html')
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return redirect('login')

# class LoginAPIView(APIView):
#     def get(self, request):
#         return render(request, 'blog/login.html')
#     def post(self, request):
#         data = request.data 
#         serializer = LoginSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
        
#         return redirect('blog/postlist-admin.html')


#board_client 페이지 렌더링
def board_client(request):
    return render(request, 'blog_app/board_client.html')

#board_admin 페이지 렌더링
def board_admin(request):
    return render(request, 'blog_app/board_admin.html')


#Form으로 로그인 화면 렌더링
def login_Form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog_app/board.html') #성공시
    else:
        form = LoginForm()
    
    return render(request, 'blog_app/login.html', {'form': form})