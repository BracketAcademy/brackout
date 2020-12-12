from rest_framework import generics, permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from django.contrib.auth import get_user_model

from .serializers import UserSerializer, AuthTokenSerializer


class UserList(generics.ListAPIView):
    """Listing all users for staff"""
    queryset = get_user_model().objects.order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)


class ManageUserView(generics.RetrieveUpdateAPIView):
    ''' Manage the authenticated user '''
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        ''' Retrieve and return authentication user '''
        return self.request.user


class CreateUser(generics.CreateAPIView):
    """Creating new user"""
    serializer_class = UserSerializer


class CreateAuthToken(ObtainAuthToken):
    """Create token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
