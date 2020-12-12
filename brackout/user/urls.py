from django.urls import path

from . import views


app_name = 'user'

urlpatterns = [
    path('get-all/', views.UserList.as_view(), name='get-all-users'),
    path('create/', views.CreateUser.as_view(), name='create-user'),
    path('me/token/', views.CreateAuthToken.as_view(), name='create-token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
