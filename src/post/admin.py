from django.contrib import admin
from post.models import Post, PostImage, PostCommentPinned


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ["id", "author", "title", "date_posted", "date_updated"]

    list_filter = ["author"]

    search_fields = ["author__username", "title"]

    list_per_page = 10


admin.site.register(Post, PostAdmin)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    model = PostImage

    list_dispaly = ["id", "post", "image", "created_at"]


class PostCommentAdmin(admin.ModelAdmin):
    model = PostCommentPinned

    list_display = ["id", "title", "content", "pinned", "post"]

    search_fields = ["author__username", "title"]

    list_per_page = 5


admin.site.register(PostCommentPinned, PostCommentAdmin)
