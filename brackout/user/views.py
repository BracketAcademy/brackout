from rest_framework import generics, permissions

from django.contrib.auth import get_user_model

from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    """Listing all users for staff"""
    queryset = get_user_model().objects.order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
