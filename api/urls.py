from django.urls import path, include
from .views import NoteViewSet
from rest_framework.routers import DefaultRouter
from .views import VerifyEmailView, RegisterView
from .views import NoteViewSet
from .views import CommentViewset
from .views import MyTokenLoginView
from .views import LogoutView



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'comments', CommentViewset)



urlpatterns = [
    # path('register/', RegisterUser.as_view(), name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('token/', MyTokenLoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='token_logout'),

]

