from .serializer import PostSerialiser, UserEngagementSerialiser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import (
    Post,
    PostImage,
    UserEngagement,
    EngagementChoices,
    UserPostTagWeightage,
)
from django.db import models
from django.conf import settings
from django.db.models import Count, Q, Case, When
from rest_framework.exceptions import APIException


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerialiser
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def create(self, request):
        """api for creating posts by admin"""

        if not request.user.is_superuser:
            return Response(
                {"message": "You donot have permission to perform this action !"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        post_insatance = Post.objects.create(
            description=validated_data["description"],
            tag=validated_data["tag"],
            created_by=request.user,
        )
        list(
            map(
                lambda image: PostImage.objects.create(
                    image=image, post=post_insatance
                ),
                validated_data.get("image"),
            )
        )
        return Response(
            dict(message="Post created successfully!"), status=status.HTTP_200_OK
        )

    def sort_by_tag_weightage(self, post_data, user):
        """method for sorting posts lists  as per users likes and dislikes"""

        for post in post_data:
            post["tag_weightage"] = (
                UserPostTagWeightage.objects.get(tag=post["tag"], user=user).weightage
                if UserPostTagWeightage.objects.filter(
                    tag=post["tag"], user=user
                ).exists()
                else 0
            )
        sorted_list = sorted(post_data, key=lambda x: x["tag_weightage"], reverse=True)
        return sorted_list

    def get_queryset(self):
        queryset = (
            Post.objects.all()
            .prefetch_related("postimage_set")
            .annotate(
                no_of_likes=Count(
                    "userengagement",
                    filter=Q(userengagement__engagement_status=EngagementChoices.LIKE),
                ),
                no_of_dislikes=Count(
                    "userengagement",
                    filter=Q(
                        userengagement__engagement_status=EngagementChoices.DISLIKE
                    ),
                ),
                user_engagement_status=Case(
                    When(
                        userengagement__user=self.request.user,
                        userengagement__engagement_status=EngagementChoices.LIKE,
                        then=EngagementChoices.LIKE,
                    ),
                    When(
                        userengagement__user=self.request.user,
                        userengagement__engagement_status=EngagementChoices.DISLIKE,
                        then=EngagementChoices.DISLIKE,
                    ),
                    default=EngagementChoices.NONE,
                    output_field=models.IntegerField(),
                ),
            )
        )
        return queryset

    def list(self, request, *args, **kwargs):
        """api for listing all posts and its details"""

        queryset = self.filter_queryset(self.get_queryset())
        response_data = []
        for post in queryset:
            image_list = []
            for post_img in post.postimage_set.all():
                if post_img.image:
                    image_list.append(f"{settings.SITE_URL}{post_img.image.url}")

            response_data.append(
                {
                    "id": post.id,
                    "description": post.description,
                    "tag": post.tag,
                    "engagement_status": post.user_engagement_status,
                    "no_of_likes": post.no_of_likes,
                    "no_of_dislikes": post.no_of_dislikes,
                    "created_by": post.created_by.username,
                    "created_at": post.created_at,
                    "updated_at": post.updated_at,
                    "images": image_list,
                }
            )

        response_data = dict(
            message=self.sort_by_tag_weightage(response_data, request.user)
        )
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="engagement")
    def engagement(self, request, pk=None):
        """api for liking and disliking post by user"""

        serializer = UserEngagementSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = request.user
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise APIException(detail="wrong post id", code=status.HTTP_404_NOT_FOUND)

        if UserEngagement.objects.filter(user=user, post=post).exists():
            user_engagement = UserEngagement.objects.get(user=user, post=post)
            if validated_data["engagement_status"] == user_engagement.engagement_status:
                if user_engagement.engagement_status == EngagementChoices.LIKE.value:
                    return Response(
                        dict(message="You have already liked this post"),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif (
                    user_engagement.engagement_status == EngagementChoices.DISLIKE.value
                ):
                    return Response(
                        dict(message="You have already disliked this post"),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        dict(message="no engagement"),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                user_engagement.engagement_status = validated_data["engagement_status"]
                user_engagement.save(update_fields=["engagement_status"])
        else:
            user_engagement = UserEngagement.objects.create(
                post=post,
                engagement_status=validated_data["engagement_status"],
                user=request.user,
            )
        if user_engagement.engagement_status == EngagementChoices.LIKE.value:
            return Response(
                dict(message="You have successfully liked this post"),
                status=status.HTTP_200_OK,
            )
        elif user_engagement.engagement_status == EngagementChoices.DISLIKE.value:
            return Response(
                dict(message="You have successfully disliked this post"),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                dict(message="successfully updated"), status=status.HTTP_200_OK
            )


    @action(detail=True, methods=["GET"], url_path="likes_dislikes")
    def get_likes_dislikes(self, request, pk=None):
        """api for geting likes and dislikes of a post"""
        
        if not request.user.is_superuser:
            return Response(
                {"message": "You donot have permission to perform this action !"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise APIException(detail="wrong post id", code=status.HTTP_404_NOT_FOUND)
        no_of_likes = UserEngagement.objects.filter(
            post=post, engagement_status=EngagementChoices.LIKE
        ).count()
        no_of_dislikes = UserEngagement.objects.filter(
            post=post, engagement_status=EngagementChoices.DISLIKE
        ).count()
        return Response(
            dict(
                id=post.id,
                description=post.description,
                tag=post.tag,
                created_at=post.created_at,
                no_of_likes=no_of_likes,
                no_of_dislikes=no_of_dislikes,
            ),
            status=status.HTTP_200_OK,
        )
