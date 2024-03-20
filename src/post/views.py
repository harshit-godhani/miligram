from datetime import datetime
from rest_framework.decorators import api_view
from django.http import HttpResponse


from post.serializer import PostSearializer
from .models import Post
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from rest_framework.views import APIView


@api_view(["GET"])
def get_post(request):
    posts = Post.objects.all()
    posts = Post.objects.filter(pk=3)

    data = []

    for post in posts:
        context = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "date_posted": post.date_posted,
            "author": post.author.username,
            "date_updated": post.date_updated,
        }

        data.append(context)

    return HttpResponse(data)


@api_view(["POST"])
def create_post(request):
    data = request.data
    post_title = data.get("title")
    post_contain = data.get("contain")

    if request.user.is_authenticated:
        post_user = request.user
    else:
        return Response(
            {"message": "login required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    print(post_user)
    print("=============")

    post = Post.objects.create(title=post_title, content=post_contain, author=post_user)
    return HttpResponse(post)


@api_view(["PATCH"])
def update_post(request):
    data = request.data

    post_id = data.get("id")
    post_title = data.get("title")
    post_contain = data.get("contain")
    if not post_id:
        return Response(
            {"message": "Post id requred"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post not found")

    try:
        user = User.objects.get(username="admin")
    except User.DoesNotExist:
        return HttpResponse("User not found")

    if user:
        post.author = user

    if post_title:
        post.title = post_title

    if post_contain:
        post.content = post_contain

    post.date_updated = timezone.now()

    post.save()


def delete_post(request):
    try:
        post = Post.objects.get(pk=5)
    except Post.DoesNotExist:
        return HttpResponse("Post not found")

    post.delete()

    return HttpResponse("Post deleted")
