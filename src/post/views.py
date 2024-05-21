from datetime import datetime
from rest_framework.decorators import api_view
from django.http import HttpResponse
from post.serializer import PostSearializer, PostImageSearializer
from post.models import Post, PostImage, PostCommentPinned
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# from django.http import JsonResponse
# import requests
# from bs4 import BeautifulSoup


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


class PostImageview(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("Post")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        imgSeralizer = PostImageSearializer(data=request.data)
        if imgSeralizer.is_valid():
            imgSeralizer.save()
            return Response(imgSeralizer.data, status=status.HTTP_200_OK)

        return Response(imgSeralizer.errors, status=status.HTTP_400_BAD_REQUEST)


# def scrape_example_domain(request):

#     url = "https://example.com"

#     response = requests.get(url)

#     if response.status_code == 200:

#         soup = BeautifulSoup(response.text, "html.parser")

#         links = soup.find_all("a")
#         for link in links:
#             print(link.get("href"))

#         # Find and extract the text content of the <title> tag
#         title = soup.title.text
#         print("Title:", title)

#         heading = soup.find("h1").text
#         paragraph = soup.find("p").text

#         return JsonResponse({"heading": heading, "paragraph": paragraph})

#     else:
#         return JsonResponse({"error": "Failed to fetch the page"}, status=500)


class PostCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("Post")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

    queryset = PostCommentPinned.objects.all()
    serializer_class = PostImageSearializer
