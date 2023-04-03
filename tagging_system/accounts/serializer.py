from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


User = get_user_model()


class UserRegister(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def save(self):
        reg = User(
            username=self.validated_data["username"],
            password=make_password(self.validated_data["password"]),
        )
        reg.save()
        return reg
