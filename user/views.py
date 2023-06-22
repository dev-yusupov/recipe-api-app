"""
Views for user API
"""
from rest_framework.generics import CreateAPIView

from user.serializers import UserSerializer

class CreateUserModel(CreateAPIView):
    serializer_class = UserSerializer
    