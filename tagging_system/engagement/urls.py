from django.urls import path, include
from .views import PostView


from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"post", PostView, basename="post")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "post/<int:pk>/engagement-status/",
        PostView.as_view({"post": "engagement"}),
        name="engagement",
    ),
    path(
        "post/<int:pk>/get-likes-dilikes/",
        PostView.as_view({"get": "get_likes_dislikes"}),
        name="get_likes_dislikes",
    ),
]
