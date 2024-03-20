from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.author) + " | " + str(self.title)
