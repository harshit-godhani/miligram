from django.contrib import admin
from post.models import Post


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ["id", "author", "title", "date_posted", "date_updated"]

    list_filter = ["author"]

    search_fields = ["author__username", "title"]

    list_per_page = 10


admin.site.register(Post, PostAdmin)
