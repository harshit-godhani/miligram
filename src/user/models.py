from django.db import models
from post.models import Post


class Friendship(models.Model):
    User = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="User")
    following = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="following"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.User}| {self.following}"
