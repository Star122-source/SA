from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import AbstractUser 
from django.db import models

class CustomUser(AbstractUser ):
    nickname = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)

    # 添加 related_name 以避免衝突
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # 修改這裡
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # 修改這裡
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

'''未完成功能
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser , on_delete=models.CASCADE)

    def __str__(self):
        return self.title
'''

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('school', '學校'),
        ('life', '生活'),
    ]
    SCHOOL_CHOICES = [
        ('ntub', '北商'),
        ('ntut', '北科'),
        ('tcut', '台科'),
    ]
    LIFE_CHOICES = [
        ('mood', '心情'),
        ('work', '工作'),
    ]
    title = models.CharField(max_length= 200)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='school') # 設定默認值
    subcategory = models.CharField(max_length=10, blank=True)  # 動態設置細分類
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add= True)
    
    class Meta:
        ordering = ('-pub_date',)

    def save(self, *args, **kwargs):
        # 如果是學校分類，檢查 subcategory 是否為學校名稱
        if self.category == 'school' and self.subcategory not in dict(self.SCHOOL_CHOICES):
            raise ValueError("學校分類的 subcategory 必須為指定的學校名稱")

        # 如果是生活分類，檢查 subcategory 是否為生活主題
        if self.category == 'life' and self.subcategory not in dict(self.LIFE_CHOICES):
            raise ValueError("生活分類的 subcategory 必須為指定的生活主題")

        # 自動生成 slug
        if not self.slug:
            base_slug = slugify(f"{self.category}-{self.subcategory}-{self.title}")
            unique_slug = base_slug
            counter = 1
            
            # 檢查 slug 是否已存在
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = unique_slug  # 使用唯一的 slug

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title