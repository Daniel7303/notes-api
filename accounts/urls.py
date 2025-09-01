from django.urls import path
from .views import MeProfileView


from .views import FollowToggleAPIView, FollowersListAPIView, FollowingListAPIView, UserListView


urlpatterns = [
    path("profile/", MeProfileView.as_view(), name='me-profile'),
    path('follow/<int:user_id>/', FollowToggleAPIView.as_view(), name='follow-toggle'),
    path('followers/', FollowersListAPIView.as_view(), name='followers-list'),
    path('following/', FollowingListAPIView.as_view(), name='following-list'),
    
    
    path('user/list/', UserListView.as_view(), name='user-list'),
    
    
    
    
    
]
