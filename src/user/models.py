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


class forgotpassword(models.Model):
    email = models.EmailField(default=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    bio = models.TextField(blank=True, max_length=500)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
