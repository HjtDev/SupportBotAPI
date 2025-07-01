from django.urls import path
from . import views


app_name = 'telegram'


urlpatterns = [
    path('connect/', views.ConnectUser.as_view(), name='connect_user'),
    path('disconnect/', views.DisconnectUser.as_view(), name='disconnect_user'),
    path('available/', views.ServerAvailable.as_view(), name='server_available'),
    path('server_load/', views.ServerLoad.as_view(), name='server_load'),
]
