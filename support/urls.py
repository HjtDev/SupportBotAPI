from django.urls import path
from . import views


app_name = 'support'

urlpatterns = [
    path('available/', views.AvailableAPIView.as_view(), name='available'),
    path('server_load/', views.ServerLoadAPIView.as_view(), name='server_load'),
    path('backup/', views.ServerBackupAPIView.as_view(), name='backup'),
    path('on/', views.ServerOnAPIView.as_view(), name='server_on'),
    path('off/', views.ServerOffAPIView.as_view(), name='server_off'),
    path('info/', views.ServerInfoAPIView.as_view(), name='server_info'),
]
