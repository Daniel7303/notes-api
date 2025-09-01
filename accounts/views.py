from django.shortcuts import render

from rest_framework import permissions, generics
from rest_framework.response import Response
from .serializers import ProfileSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Follow
from .serializers import UserMiniSerializer
# Create your views here.


from .serializers import UserListSerializer

User = get_user_model()

class MeProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get_object(self):
        return self.request.user.profile
    
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    
    
    
class FollowToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target )
        if created:
            return Response({'detail': 'Followed.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already following.'}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        deleted_count, _ = Follow.objects.filter(follower=request.user, following=target).delete()
        if deleted_count:
            return Response({'detail': 'Unfollowed.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not following.'}, status=status.HTTP_400_BAD_REQUEST)
    

class FollowersListAPIView(ListAPIView):
    serializer_class = UserMiniSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        follower_ids = Follow.objects.filter(following=self.request.user).values_list('follower_id', flat=True)
        return User.objects.filter(id__in=follower_ids)


class FollowingListAPIView(ListAPIView):
    serializer_class = UserMiniSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        following_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)
        return User.objects.filter(id__in=following_ids)


class UserListView(generics.ListAPIView):
    # serializer_class = UserListSerializer
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
    
    