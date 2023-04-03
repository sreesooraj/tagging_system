from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import EngagementChoices


User = get_user_model()


class PostSerialiser(serializers.Serializer):
    """Serializer for validating posts created by admin"""

    description = serializers.CharField(required=True)
    tag = serializers.CharField(required=True)
    image = serializers.ListField(child=serializers.ImageField(), required=True)


class UserEngagementSerialiser(serializers.Serializer):
    """serialiser for validating user post engagement status upfdates"""

    engagement_status = serializers.ChoiceField(choices=EngagementChoices.choices)