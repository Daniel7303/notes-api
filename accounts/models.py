from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # use email instead of username
    REQUIRED_FIELDS = []  # for createsuperuser command
    
    
    
    
    def __str__(self):
        return self.email
    

# stores avatar
def avatar_upload_to(instance, filename):
    return f"avatars/{instance.user_id}/{filename}"


class Profile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.CharField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)
    
    
    def __str__(self):
        return f"Profile({self.user})"
    
    
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_relations', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower_relations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    
    class Meta:
        unique_together =('follower', 'following')
        ordering = ['-created_at']
        
    
    def clean(self):
        if self.follower == self.following:
            raise ValidationError("you cannot follow yourself.")
        
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.follower} follows (self.following)"
    
        
    
    