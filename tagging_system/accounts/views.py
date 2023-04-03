from django.shortcuts import render

# Create your views here.
from .serializer import UserRegister
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class Register(APIView):
    def post(self, request):
        """Api for user registration"""
        serializer = UserRegister(data=request.data)
        data = {}
        if serializer.is_valid():
            user_object = serializer.save()

            data["response"] = "registered"
            data["username"] = user_object.username
            token, _ = Token.objects.get_or_create(user=user_object)

            data["token"] = token.key
        else:
            data = serializer.errors
        return Response(data)
