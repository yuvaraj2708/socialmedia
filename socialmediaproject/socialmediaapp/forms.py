from django import forms
from .models import UserProfile, Post, Comment

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'website']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'video','caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
