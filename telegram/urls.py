from django.urls import path
from . import views


app_name = 'telegram'


urlpatterns = [
    path('connect/', views.ConnectUser.as_view(), name='connect_user'),
]
