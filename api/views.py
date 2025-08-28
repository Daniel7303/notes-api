from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework import viewsets
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

import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings


from .permisions import IsOwner
from .serializers import NoteSerializer
from .models import Note
from .serializers import UserRegisterSerializer
from .models import Comment
from .serializers import CommentSerializer

from .throttles import BurstRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import MyTokenObtainPairSerializer



# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('created_at')
    
    note = Note.objects.get(id=1)
    note.total_comment()
    
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']
    
    
    # permission_classes = [AllowAny]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by("-created_at")
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    throttle_classes = [BurstRateThrottle]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

# def send_verification_email_sendgrid(user, request):
#     from django.utils.http import urlsafe_base64_encode
#     from django.utils.encoding import force_bytes
#     from django.contrib.auth.tokens import default_token_generator
#     from django.contrib.sites.shortcuts import get_current_site

#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)
#     current_site = get_current_site(request)
#     verification_link = f"http://{current_site.domain}/api/verify-email/{uid}/{token}/"

#     message = Mail(
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to_emails=user.email,
#         subject="Verify your email",
#         plain_text_content=f"Click the link to verify your email:\n{verification_link}",
#     )

#     try:
#         sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
#         response = sg.send(message)
#         print(f"✅ Email sent to {user.email}. Status code: {response.status_code}")
#     except Exception as e:
#         print("❌ Failed to send email via SendGrid:", e)

    
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer  # DRF serializer for registration

    def perform_create(self, serializer):
        # Save user but don't activate yet
        user = serializer.save(is_active=False)
        self.send_verification_email(user)
        # send_verification_email_sendgrid(user, self.request)
    

    def send_verification_email(self, user):
        # Create email verification token and encoded UID
        uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encodes user ID to base64
        token = default_token_generator.make_token(user)  # Create time-limited secure token

        # Get the current site domain to use in the email link
        current_site = get_current_site(self.request)

        # Build the verification link
        verification_link = f"http://{current_site.domain}/api/verify-email/{uid}/{token}/"

        # Send the email
        email = EmailMessage(
            subject="Verify your email",
            body=f"Click the link to activate your account: {verification_link}",
            to=[user.email]
        )
        
        try:
            email.send()
            print("Sending verification email to:", user.email)
        except Exception as e:
            print("Failed to send email:", e)

    def create(self, request, *args, **kwargs):
        # This method is triggered on POST to /register/
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"detail": "Account created. Check your email to verify your account."},
            status=status.HTTP_201_CREATED
        )

        




class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            # Decode the UID from base64 and get user
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            # Check if the token is valid for this user
            if default_token_generator.check_token(user, token):
                user.is_active = True  # Activate user
                user.save()

                # Create or get a token (DRF token auth)
                token, _ = Token.objects.get_or_create(user=user)

                return HttpResponse(f"Email verified. Token: {token.key}")
            else:
                return HttpResponse("Invalid or expired verification link.")
        except Exception as e:
            return HttpResponse("Verification failed.")


        
        
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