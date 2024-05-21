from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .utils import get_tokens_for_user
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from user.serializer import forgotpasswordSerializer, ProfileSerializer

from rest_framework.permissions import IsAuthenticated


class UserCreateView(APIView):
    def post(self, request):
        data = request.data
        try:
            username = data["username"]
            email = data["email"]
            password = data["password"]
        except Exception as key:
            return Response({str(key): ["filed required"]})

        if User.objects.filter(username=username).exists():
            return Response({"username": ["this user already exists"]}, status=400)

        user = User.objects.create(email=email, username=username)
        user.set_password(password)
        user.save()
        # PostPermission.objects.create(user=user)

        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        ) as connection:
            recipient_list = ["godhaniharshit871@gmail.com"]
            subject = "Test Email"
            email_from = settings.EMAIL_HOST_USER
            message = "Error!"
            EmailMessage(
                subject, message, email_from, recipient_list, connection=connection
            ).send()

        res = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        return Response({"message": "User created", "user": res})


class UserLoginView(APIView):
    def post(self, request):
        data = request.data
        user_name = data["username"]
        password = data["password"]

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if authenticate(username=user_name, password=password):

            token = get_tokens_for_user(user)

            return Response({"token": token}, status=200)

        else:
            return Response(
                {"message": "Invalid Credientials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            Token.objects.get(user=request.user)
            Token.delete()
            return Response({"message": "user logout"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(
                {"message": "user already logout"}, status=status.HTTP_404_NOT_FOUND
            )


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        current_password = data["current_password"]
        new_password = data["new_password"]
        conform_password = data["conform_password"]
        if authenticate(username=request.user.username, password=current_password):
            if new_password == conform_password:
                request.user.set_password(new_password)
                request.user.save()
                return Response(
                    {"message": "successfully changed password"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "new password are not same"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": "invalid password"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserForgotPasswordView(APIView):
    serializer_class = forgotpasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                return Response({"message": "Password reset email sent."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateAPIView(APIView):
    def put(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
