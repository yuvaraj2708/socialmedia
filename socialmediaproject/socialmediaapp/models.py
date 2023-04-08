from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)




class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
  
    def has_module_perms(self, app_label):
        return True



User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.user.email


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts', null=True, blank=True)  # Update to ImageField
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)  # Add a new FileField for video
    caption = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')

    def __str__(self):
        return f'{self.user.email}: {self.caption[:10]}'
    
    @property
    def getuserprofile(self):
        profile = UserProfile.objects.get(user=self.user)
        return profile


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}: {self.text[:10]}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user} likes {self.post}'

    
    ...

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower.email} follows {self.followed.email}'


user = CustomUser.objects.get(email='admin@gmail.com')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Like, blank=True)
    posts = models.ManyToManyField(Post, blank=True)
    follows = models.ManyToManyField(Follow, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} Notification'

    class Meta:
        ordering = ('-created_date', )

    @receiver(post_save, sender=Like)
    def create_like_notification(sender, instance, created, **kwargs):
     if created:
        notification = Notification.objects.create(user=instance.post.user)
        notification.likes.add(instance)
        notification.save()

# signal to create notification for new follow
    @receiver(post_save, sender=Follow)
    def create_follow_notification(sender, instance, created, **kwargs):
     if created:
        notification = Notification.objects.create(user=instance.followed)
        notification.follows.add(instance)
        notification.save()
  



# signal to create notification for new comment
    @receiver(post_save, sender=Comment)
    def create_comment_notification(sender, instance, created, **kwargs):
     if created:
        notification = Notification.objects.create(user=instance.post.user)
        notification.comments.add(instance)
        notification.save()



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    
