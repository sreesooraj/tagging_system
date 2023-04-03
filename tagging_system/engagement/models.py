from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.conf import settings
import os


User = get_user_model()


class Post(models.Model):
    """Model for saving posts created by admin"""

    description = models.TextField(blank=True, max_length=1000)
    tag = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    user_engagement = models.ManyToManyField(
        User, through="UserEngagement", related_name="user_engagement"
    )


def upload_to(instance, filename):
    """Function to get the directory path for storing post images"""
    return os.path.join(settings.MEDIA_ROOT, "posts", str(instance.post.id), filename)


def get_absolute_image_url(instance):
    """Function for retriving absalute url of post images"""
    return f"{settings.SITE_URL}{instance.image.url}"


class PostImage(models.Model):
    """Model for saving images of post"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to)

    @property
    def absolute_image_url(self):
        """property method for retrieving absaolute url of post images"""
        return get_absolute_image_url(self)


class EngagementChoices(models.IntegerChoices):
    """Choices for user engagement status like LIKE and Dislike"""

    NONE = 3
    LIKE = 1
    DISLIKE = 2


class UserEngagement(models.Model):
    """Model for saveing user engagement"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    engagement_status = models.IntegerField(
        choices=EngagementChoices.choices, default=EngagementChoices.NONE
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class UserPostTagWeightage(models.Model):
    """Model for saving weightage of posts as per liked and disliked by user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, null=True)
    weightage = models.IntegerField(default=0)
