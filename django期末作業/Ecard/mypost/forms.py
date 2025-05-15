from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Post

class CustomUserCreationForm(UserCreationForm):  
    class Meta:
        model = CustomUser    
        fields = ('username', 'password1', 'password2', 'nickname', 'avatar', 'bio')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields = ('nickname', 'avatar', 'bio')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'subcategory', 'body')
