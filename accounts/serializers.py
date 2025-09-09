from rest_framework import serializers, generics
from django.contrib.auth import get_user_model
from .models import Profile
from .models import Follow


User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'bio', 'is_following']
        
    
    def get_avatar(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and getattr(profile, 'avatar', None):
            request = self.context.get('request')
            url = profile.avatar.url
            return request.build_absolute_uri(url) if request else url
        return None
    
    def get_bio(self, obj):
        profile = getattr(obj, 'profile', None)
        return getattr(profile, 'bio', '') if profile else ''
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(follower=request.user, following=obj).exists()
        

class ProfileSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['user', 'name', 'bio', 'location', 'birth_date', 'avatar', 'followers_count', 'following_count', 'is_following']
        read_only_fields = ['user']
        
        
    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj.user).count()
    
    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj.user).count()
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(follower=request.user, following=obj.user).exists()




# Get all user list, id included
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        
