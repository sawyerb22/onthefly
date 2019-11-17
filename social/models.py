from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from core.models import BaseModel
from user.models import Profile


class Post(BaseModel):
    user = models.ForeignKey(
        Profile, verbose_name="Created By", on_delete=models.CASCADE, related_name="user_photos"
    )
    caption = models.TextField(max_length=500, blank=True)
    photo = ProcessedImageField(
        upload_to="user_photos",
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1200, height=1200)],
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Photo on {self.date_created}"

    class Meta:
        """Metadata."""

        ordering = ["-date_created"]


class Like(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}{self.id} Like"

    class Meta:
        unique_together = (("user", "post"))
        ordering = ["-date_created"]


class Comment(models.Model):
    """A comment on a post."""

    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")

    content = models.TextField(max_length=2000)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        """Metadata."""

        ordering = ["-date_created"]
