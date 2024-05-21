from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.author) + " | " + str(self.title)


class PostImage(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.Post.title) + " | " + str(self.image)


class PostCommentPinned(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pinned = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    # content = models.TextField()

    def __str__(self) -> str:
        return str(self.post.title) + "  |  " + str(self.pinned)


# class PostSave(models.Model):
