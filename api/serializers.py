from .models import Note
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Comment



User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'note', 'user', 'text', 'created_at']
        

class NoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'created_at', 'total_comment', 'comments']
        
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters")
        return value
    
    def validate(self, data):
        if "django" in data.get('content', '').lower() and "drf" not in data.get('content', '').lower():
            raise serializers.ValidationError("If you mention 'Django', you must also mention 'DRF'.")
        return data
    
    

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, label="Comfirm Password")
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
    
    def validate(seld, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": 'passwords must match'})
        return data
        
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        is_active = validated_data.pop('is_active', True)  # get it safely
        
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = is_active  # ✅ this now works
        user.save()
        return user

    
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise serializers.ValidationError("Email not verified")
        
        return data
                     
        