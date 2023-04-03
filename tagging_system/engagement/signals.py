from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserEngagement, UserPostTagWeightage, Post, EngagementChoices


@receiver(post_save, sender=UserEngagement)
def update_user_engagement(sender, instance, created, **kwargs):
    """signal method for updating tag weightage while user likes and dislikes posts"""

    obj, _ = UserPostTagWeightage.objects.get_or_create(
        user=instance.user, tag=instance.post.tag
    )
    old_instance = UserEngagement.objects.get(id=instance.id)
    if instance.engagement_status == EngagementChoices.LIKE:
        obj.weightage = obj.weightage + 1
    elif instance.engagement_status == EngagementChoices.DISLIKE:
        obj.weightage = obj.weightage - 1
    elif old_instance.engagement_status == EngagementChoices.LIKE:
        obj.weightage = obj.weightage - 1
    elif old_instance.engagement_status == EngagementChoices.DISLIKE:
        obj.weightage = obj.weightage + 1
    obj.save()
