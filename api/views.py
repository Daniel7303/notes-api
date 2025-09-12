from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework import viewsets
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from django.utils.encoding import force_str

from algoliasearch_django import raw_search
import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.shortcuts import get_object_or_404


from .permisions import IsOwner
from rest_framework.decorators import action

from .serializers import NoteSerializer
from .models import Note
from .serializers import UserRegisterSerializer

from .models import Comment
from .serializers import CommentSerializer

from .models import Like
from .serializers import LikeSerializer
from .models import CommentLike
from . serializers import CommentLikeSerializer

from .models import Note
from accounts.models import Follow

from .serializers import NoteFeedSerializer

from accounts.models import Profile

from .throttles import BurstRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import MyTokenObtainPairSerializer



# Create your views here.


User = get_user_model()


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def comments_count(self, request, pk=None):
        note = self.get_object()  # fetch the note by pk
        return Response({"total_comments": note.total_comment()})
    
    
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    throttle_classes = [BurstRateThrottle]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    




class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data  

        # Extract password safely
        password = validated_data.pop("password")
        validated_data.pop("password2", None)

        # Check if email already exists
        existing_user = User.objects.filter(email=validated_data["email"]).first()

        if existing_user:
            if existing_user.is_active:
                # Case 1: Email already verified/active → stop
                raise serializers.ValidationError(
                    {"email": "A user with this email already exists and is verified."}
                )
            else:
                # Case 2: User exists but not active → resend verification
                user = existing_user
                user.set_password(password)
                user.save()
                print("Resending verification email to inactive user:", user.email)
        else:
            # Case 3: Create new inactive user
            user = User(**validated_data)
            user.is_active = False
            user.set_password(password)
            user.save()

        # Always send verification email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.request)
        verification_link = f"http://{current_site.domain}/api/verify-email/{uid}/{token}/"
        email = EmailMessage(
            subject="Verify your email",
            body=f"Click the link to activate your account: {verification_link}",
            to=[user.email]
        )

        try:
            email.send(fail_silently=False)
        except Exception as e:
            print("Email sending failed:", e)
            raise serializers.ValidationError(
                {"email": "Could not send verification email. Please try again."}
            )

        return user  # return user for `create()`

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        return Response(
            {"message": f"Account created for {user.email}. Check your email to verify your account."},
            status=status.HTTP_201_CREATED
        )



class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                # Create JWT tokens
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "detail": "Email verified successfully.",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"detail": "Invalid or expired verification link."}, status=status.HTTP_400_BAD_REQUEST)

        except get_user_model().DoesNotExist:
            return Response({"detail": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Verification error:", e)
            return Response({"detail": "Verification failed."}, status=status.HTTP_400_BAD_REQUEST)



        
        
class MyTokenLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
       
       

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"details": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        

            

class LikeNoteView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        note_id = self.kwargs.get("pk")
        user = self.request.user

        # prevent duplicate likes
        like, created = Like.objects.get_or_create(
            note_id=note_id,
            user=user,
        )
        if not created:
            like.delete()  # toggle unlike
            
            
            
class LikeCommentView(generics.GenericAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user

        # prevent duplicate likes
        like, created = CommentLike.objects.get_or_create(
            comment=comment,
            user=user,
        )
        if not created:
            like.delete()  # toggle unlike
            return Response({"message": "Unliked comment"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "Liked comment"}, status=status.HTTP_201_CREATED)
        
        




class FeedView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteFeedSerializer

    def get_queryset(self):
        # Get all users current user follows
        following_users = Follow.objects.filter(
            follower=self.request.user
        ).values_list("following", flat=True)

        # Fetch notes from those users, order by latest
        return Note.objects.filter(user__in=following_users).order_by("-created_at")
    
    
    
    class SearchApiView(APIView):
        def get(self, request):
            query = request.Get.get('q', '')
            results = raw_search(Note, query)
            return Response(results)
        
        def get(self, request):
            query = request.Get.get('q', '')
            results = raw_search(Profile, query)
            
            return Response(results)