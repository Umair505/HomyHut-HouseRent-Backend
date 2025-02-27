from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import UserAccount
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserAccountSerializer, UserProfileSerializer,
    AllUserSerializer, AdminMessageSerializer, UserStaffSerializer
)
from .permissions import IsAdminOrReadOnly 
from rest_framework.permissions import IsAdminUser

User = get_user_model()

class UserRegistrationSerializerViewSet(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'You are already logged in'}, status=400)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"https://homyhut-houserent-backend.onrender.com/api/user/activate/{uid}/{token}/"

            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                'email_verification.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")

            email.send()

            return Response('Check your email for confirmation')
        return Response(serializer.errors)

User = get_user_model()

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
    except (TypeError, ValueError, UnicodeDecodeError):
        return redirect('verified_unsuccess')

    user = get_object_or_404(User, pk=uid)

    if default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
        return redirect('login')
    else:
        return redirect('register')

# ✅ User Login View
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'You are already logged in'}, status=400)
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'is_staff': user.is_staff
                })
            return Response({'error': 'Invalid Credentials'}, status=400)
        return Response(serializer.errors, status=400)

# ✅ User Logout View
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Successfully logged out'})

# ✅ User Profile View
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=400)

# ✅ User List View (Admin Only)
class AllUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AllUserSerializer
    permission_classes = [IsAdminOrReadOnly]

# ✅ User Account View
class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAdminOrReadOnly]

# ✅ Manage Staff Users (Admin Only)
class UserStaffViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserStaffSerializer
    permission_classes = [IsAuthenticated]

# ✅ Admin Message View
class AdminMessageViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = AdminMessageSerializer
    permission_classes = [IsAuthenticated]
