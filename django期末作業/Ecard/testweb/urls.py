from django.contrib import admin
from django.urls import path
from mypost.views import Homepage, school_posts, life_posts, post_detail, profile, register, login_view, logout_view, upload_avatar, edit_profile
from django.conf import settings
from django.conf.urls.static import static
from mypost.views import add_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Ecard', Homepage, name='homepage'),  # 主頁
    path('school/<str:school_name>/', school_posts, name='school_posts'),  # 學校分類貼文
    path('life/<str:life_topic>/', life_posts, name='life_posts'),  # 生活分類貼文
    path('post/<slug:slug>/', post_detail, name='post_detail'),  # 貼文詳情
    path('my/', profile, name='profile'),  # 個人檔案
    path('register/', register, name='register'),  # 註冊
    path('login/', login_view, name='login'),  # 登入
    path('logout/', logout_view, name='logout'),  # 登出
    path('upload_avatar/', upload_avatar, name='upload_avatar'),  # 上傳頭像
    path('edit_profile/', edit_profile, name='edit_profile'),  # 修改個人資訊
    path('add_post/', add_post, name='add_post'),  # 新增貼文
]

# 媒體文件路由
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)