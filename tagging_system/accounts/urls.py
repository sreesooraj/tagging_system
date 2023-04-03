from django.urls import path

from .views import Register
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("register", Register.as_view(), name="register"),
    path("login/", obtain_auth_token, name="login"),
]
