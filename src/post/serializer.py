from rest_framework import serializers
from .models import Post, PostImage, PostCommentPinned


class PostSearializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"


class PostImageSearializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"


class PostCommentSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = PostCommentPinned
        fields = ["id", "content"]
