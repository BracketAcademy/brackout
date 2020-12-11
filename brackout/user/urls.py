from django.urls import path

from .views import UserList


app_name = 'user'

urlpatterns = [
    path('get-all/', UserList.as_view(), name='get-all-users'),
]
