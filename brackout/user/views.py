from rest_framework import generics, permissions, authentication, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, AuthTokenSerializer


class UserList(generics.ListAPIView):
    """Listing all users for staff"""
    queryset = get_user_model().objects.order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
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


class VerifyUser(APIView):
    """Activate user's account"""
    def get(self, request, uidb64, token):
        try:
            id_decoded = urlsafe_base64_decode(force_text(uidb64))
            user = get_user_model().objects.get(pk=id_decoded)
        except Exception:
            user = None
        if user:
            user.is_active = True
            user.save()
            return Response(data=UserSerializer(user).data)
        else:
            return Response(
                data={'error': _('Invalid Activation Link')},
                status=status.HTTP_400_BAD_REQUEST)


class CreateAuthToken(ObtainAuthToken):
    """Create token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
