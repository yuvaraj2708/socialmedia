from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, profile, post_create, post_detail, post_like, user_follow,search,userprofile,camera,notifications
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<str:email>/', profile, name='profile'),
    path('post/create/', post_create, name='post_create'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', post_like, name='post_like'),
    path('user/<str:email>/follow/', user_follow, name='user_follow'),
    path('search/',search,name='search'),
    path('userprofile/<str:email>/',userprofile,name='userprofile'),
    path('camera/',camera,name='camera'),
    path('notifications/', notifications, name='notifications'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


