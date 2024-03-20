from django.contrib import admin
from .models import Friendship


class FriendshipAdmin(admin.ModelAdmin):
    model = Friendship

    list_display = ["User", "created_at"]


admin.site.register(Friendship, FriendshipAdmin)
