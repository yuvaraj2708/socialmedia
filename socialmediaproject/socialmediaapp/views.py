from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import UserProfile, Post, Comment, Like, Follow
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import UserProfileSerializer,PostSerializer,CommentSerializer,LikeSerializer,FollowSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import CustomUser, Follow,Notification


User = get_user_model()

@login_required


def home(request):
    # get all posts from users followed by the logged in user
    following = Follow.objects.filter(follower=request.user).values_list('followed__id', flat=True)
    posts = Post.objects.filter(user__in=following).order_by('-created_date')
    return render(request, 'home.html', {'posts': posts, 'user': request.user})


@login_required
def profile(request, email):
    user = User.objects.get(email=email)
    profile = UserProfile.objects.get(user=user)
    posts = Post.objects.filter(user=user).order_by('-created_date')
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})
    

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by('-created_date')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form, 'comments': comments})



@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like= Like.objects.get_or_create(user=request.user, post=post)
    created= Like.objects.get_or_create(user=request.user, post=post)
    print(f"Like object created: {created}")
    
    if not created:
        like.delete()
    return HttpResponseRedirect(reverse('post_detail', args=[str(post_id)]))

@login_required
def user_follow(request, email):
    user = User.objects.get(email=email)
    follow, created = Follow.objects.get_or_create(follower=request.user, followed=user)
    if not created:
        follow.delete()
    return redirect('profile', email=email)




def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def search(request):
    query = request.GET.get('q')
    query = request.GET.get('query')
    if query:
        users = User.objects.filter(email__icontains=query)
        following = Follow.objects.filter(follower=request.user).values_list('followed__id', flat=True)
        return render(request, 'search.html', {'users': users, 'following': following, 'query': query})
    return render(request, 'search.html')


def userprofile(request, email):
    user = User.objects.get(email=email)
    posts = Post.objects.filter(user=user).order_by('-created_date')
    following = Follow.objects.filter(follower=request.user, followed=user).exists()
    return render(request, 'userprofile.html', {'user': user, 'posts': posts, 'following': following,'profile':profile})


def camera(request):
    return render(request,"camera.html")

def notifications(request):
    # Get all notifications for the logged in user
    notifications = Notification.objects.filter(user=request.user)

    # Mark all notifications as read
    notifications.update(read=True)

    context = {
        'notifications': notifications
    }

    return render(request, 'notifications.html', context)

class profileApiView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_class = [IsAuthenticated ] 
    

class PostApiView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated ] 


class CommentApiView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated ] 

    
class LikeApiView (ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = UserProfileSerializer
    permission_class = [IsAuthenticated ] 


class FollowApiView(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_class = [IsAuthenticated ] 
 