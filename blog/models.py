from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Meta:
        ordering = ("-publish_date",)
        indexes = (
            models.Index(fields=["-publish_date"]),
        )

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish_date")
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now())
    created_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail",
                       args=[self.publish_date.year, self.publish_date.month, self.publish_date.day, self.slug])


class Comment(models.Model):

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"])
        ]

    class Status(models.TextChoices):
        ACTIVE = "AC", "Active"
        DISABLED = "DB", "Disabled"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
