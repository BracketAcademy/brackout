from django.urls import path

from . import views
from . import google_views

app_name = 'user'

urlpatterns = [
    path('get-all/', views.UserList.as_view(), name='get-all-users'),
    path('create/', views.CreateUser.as_view(), name='create-user'),
    path('me/token/', views.CreateAuthToken.as_view(), name='create-token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path(
        'activation/<uidb64>/<token>/',
        views.VerifyUser.as_view(),
        name='user-activation'),
    path(
        'google-auth',
        google_views.GoogleAuthorization.as_view(),
        name='google-auth'),
    path(
        'google-redirect',
        google_views.GoogleRedirect.as_view(),
        name='google-redirect')
]
