from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime

from django.contrib.auth import authenticate

from django.core.mail import EmailMessage, get_connection
from django.conf import settings


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
            message = "Hello How are you? Khana ke jana ha"
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

            token, created = Token.objects.update_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)

            response = {
                "username": user.username,
                "email": user.email,
                "usertype": "admin",
                "token": str(token),
            }
            return Response(response, status=200)
        return Response(
            {"message": "Invalid Credientials"}, status=status.HTTP_401_UNAUTHORIZED
        )
