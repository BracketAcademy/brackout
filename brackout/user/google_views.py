from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow

from os import getcwd
from json import loads

from .serializers import OAuthSerializer


def obtain_flow(request):
    domain = get_current_site(request).domain
    flow = Flow.from_client_secrets_file(
        getcwd()+'/user/bull.json',
        scopes=[
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri='http://'+domain+reverse('user:google-redirect')
    )
    return flow


def get_user_info(request, flow):
    code = request.GET['code']
    flow.fetch_token(code=code)
    auth_token = flow.credentials.id_token
    try:
        user_info = id_token.verify_oauth2_token(
                auth_token, requests.Request())
        if 'accounts.google.com' in user_info['iss']:
            return user_info
    except Exception:
        raise Exception("Invalid or Expired Token.")


def get_password():
    with open(settings.BASE_DIR / 'bullshit.json', 'r') as secs:
        secs = loads(secs.read())
        return secs['django']['SOCIAL_PASS']


class GoogleAuthorization(APIView):
    """Get User Credentials From Google API"""
    def get(self, request):
        flow = obtain_flow(request)
        auth_uri = flow.authorization_url()
        return redirect(auth_uri[0])


class GoogleRedirect(APIView):
    """Finalize Authentication"""
    def get(self, request):
        try:
            request.GET['code']
        except Exception:
            return Response(
                data={'error': "Invalid Token!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        flow = obtain_flow(request)
        try:
            user_info = get_user_info(request, flow)
            data = {
                'email': user_info['email'],
                'password': get_password(),
                'name': user_info['name'],
                'auth_provider': 'GO',
            }

            serializer = OAuthSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                token, created = Token.objects.get_or_create(
                    user=get_user_model().objects.get(
                        email=serializer.data['email']
                    )
                )
                data.update({'token': str(token)})
                data.pop('password')
                return Response(
                    data,
                    status=status.HTTP_201_CREATED)
            return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                data={
                    'email':
                    'user with this Email Address already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                data={'error': str(type(e))},
                status=status.HTTP_400_BAD_REQUEST
            )
