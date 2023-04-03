"""socialmediaproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from socialmediaapp.views import (
    PostApiView,
    CommentApiView,
    LikeApiView,
    FollowApiView,
    profileApiView,
)

router = DefaultRouter()
router.register(r'posts', PostApiView, basename='post')
router.register(r'comments', CommentApiView, basename='comment')
router.register(r'likes', LikeApiView, basename='like')
router.register(r'follows', FollowApiView, basename='follow')
router.register(r'profiles', profileApiView, basename='profile')

urlpatterns = [
    path('', include('socialmediaapp.urls')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]

