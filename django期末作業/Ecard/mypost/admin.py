from django.contrib import admin
from mypost.models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'body', 'pub_date')
    
admin.site.register(Post, PostAdmin)