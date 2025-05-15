from django.shortcuts import render
from django.http import HttpResponse
from mypost.models import Post,CustomUser
from datetime import datetime 
from django.shortcuts import render, get_object_or_404

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, PostForm
# Create your views here.
#登出帳號
def logout_view(request):
    logout(request)
    return redirect('homepage')  # 登出後重定向到主頁

#登入帳號
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')  # 登入成功後重定向
        else:
            messages.error(request, "用戶名或密碼錯誤")  # 顯示錯誤消息

    return render(request, 'login.html')  # 返回登入頁面

#註冊帳號
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
        else:
            messages.error(request, "註冊失敗，請檢查您的輸入。")  # 失敗消息
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

#上傳頭像
def upload_avatar(request):
    if request.method == 'POST':
        avatar = request.FILES['avatar']
        user = request.user
        user.avatar = avatar
        user.save()
        return redirect('profile')
    return redirect('profile')

#修改個人資訊
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # 修改成功後重定向到個人檔案頁面
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

#新增貼文
@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 設置作者為當前用戶
            post.save()
            return redirect('homepage')  # 新增成功後重定向到主頁
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

def Homepage(request):
    return render(request, 'homepage.html')

def school_posts(request, school_name):
    posts = Post.objects.filter(category='school', subcategory=school_name)
    return render(request, 'school_posts.html', {'posts': posts, 'school_name': school_name})

def life_posts(request, life_topic):
    posts = Post.objects.filter(category='life', subcategory=life_topic)
    return render(request, 'life_posts.html', {'posts': posts, 'life_topic': life_topic})

def post_detail(request, slug):
    try:
        #get 預設一定會拿到一筆資料
        post = Post.objects.get(slug = slug)
        return render(request, 'post.html', locals())
    except:
        return HttpResponse("錯誤")

def profile(request):
    return render(request, 'profile.html')

    
