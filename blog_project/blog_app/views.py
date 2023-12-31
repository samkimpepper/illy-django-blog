from django.shortcuts import render, redirect,get_object_or_404
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .forms import LoginForm,ArticleForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from django.conf import settings
from django.views import View 
from django.http import JsonResponse
from django.core.files.storage import default_storage

from .models import Article
import openai

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


#post_list 페이지 렌더링 
def post_list(request):
    posts = Article.objects.filter(publish='Y').order_by('-views')

    return render(request, 'blog_app/post_list.html', {'posts': posts})

#board 페이지 렌더링
def board(request):
    return render(request, 'blog_app/board.html')


#Form으로 로그인 화면 렌더링 by 오준경
def login_Form(request):
    # 이미 로그인한 경우
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    
    else:
        form = LoginForm(data=request.POST or None)
        if request.method == "POST":

            # 입력정보가 유효한 경우 각 필드 정보 가져옴
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # 위 정보로 사용자 인증(authenticate사용하여 superuser로 로그인 가능)
                user = authenticate(request, username=username, password=password)

                # 로그인이 성공한 경우
                if user is not None:
                    login(request, user) # 로그인 처리 및 세션에 사용자 정보 저장
                    return redirect('blog:post_list')  # 리다이렉션
        return render(request, 'blog_app/login.html', {'form': form}) #폼을 템플릿으로 전달
    

# by 이진혁
def post_detail(request, post_id):
    post = get_object_or_404(Article, id=post_id)

    if request.method == 'POST': 
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('blog:post_list')

    post.views += 1 
    post.save() 

    previous_post = Article.objects.filter(id__lt=post.id, publish='Y').order_by('-id').first()
    next_post = Article.objects.filter(id__gt=post.id, publish='Y').order_by('id').first()

    recommended_posts = Article.objects.filter(topic=post.topic, publish='Y').exclude(id=post.id).order_by('-published_at')[:2]
    for recommended_post in recommended_posts:
        soup = BeautifulSoup(recommended_post.content, 'html.parser')
        image_tag = soup.find('img')
        recommended_post.image_tag = str(image_tag) if image_tag else ''
    
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'recommended_posts': recommended_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'blog_app/board.html', context)




#게시글 작성, 수정 페이지, 임시저장 글 존재시 불러옴  by 이채림



@login_required #로그인 할때만 접근할 수 있게 by 오준경
def write(request, post_id=None):
    article_id = post_id

    if article_id:
        article = get_object_or_404(Article, id=article_id)
    else:
        article = Article.objects.filter(author_id=request.user.id, publish='N').order_by('-published_at').first()

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        print(form)
        if form.is_valid():

            article = form.save(commit=False)

            if not form.cleaned_data.get('topic'):
                article.topic = '전체'
            
            if 'temp-save-button' in request.POST:
                article.publish = 'N'
            else:
                article.publish = 'Y'

            article.author_id = request.user.id 
            article.save()
            return redirect('blog:board', post_id=article.id)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form, 'article': article, 'edit_mode': article_id is not None}

    return render(request, 'blog_app/write.html', context)

class image_upload(View):
    def post(self, request):
        file = request.FILES['file']
        filepath = 'uploads/' + file.name 
        filename = default_storage.save(filepath, file)
        file_url = '/blog/media/' + filename 


        return JsonResponse({'location': file_url})


# post_list 뷰와 비슷하게 필터링된 게시물 목록을 보여주는 뷰를 추가 by 이진혁
def filtered_post_list(request, category):
    
    # category에 따라 게시물 필터링
    if category == '전체':
        posts = Article.objects.filter(publish='Y').order_by('-views')
    else:
        posts = Article.objects.filter(topic=category, publish='Y').order_by('-views')

    return render(request, 'blog_app/post_list.html', {'posts': posts})


# 포스트리스트
def post_list(request, topic=None):
    
    # 특정 주제로 필터링
    if topic:
        posts = Article.objects.filter(topic=topic, publish='Y').order_by('-views')
    
    else:
        posts = Article.objects.filter(publish='Y').order_by('-views') 
    return render(request, 'blog_app/post_list.html', {'posts': posts})


#자동완성기능
openai.api_key = settings.API_KEY 

def autocomplete(request):
    if request.method == "POST":

        #제목 필드값 가져옴
        prompt = request.POST.get('title')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            # 반환된 응답에서 텍스트 추출해 변수에 저장
            message = response['choices'][0]['message']['content']
        except Exception as e:
            message = str(e)
        return JsonResponse({"message": message})
    return render(request, 'autocomplete.html')