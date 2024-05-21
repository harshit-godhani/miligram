from django.contrib import admin
from .models import Friendship, Profile


class FriendshipAdmin(admin.ModelAdmin):
    model = Friendship

    list_display = ["User", "created_at"]


admin.site.register(Friendship, FriendshipAdmin)


class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
        fields = ["user", "bio", "location", "birth_date"]

        search_fields = ["user__username", "location"]

        list_filter = ["author"]

        list_per_page = 10


admin.site.register(Profile, ProfileAdmin)
