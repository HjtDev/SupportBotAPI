from django.urls import path
from . import views


app_name = 'support'

urlpatterns = [
    path('available/', views.AvailableAPIView.as_view(), name='available'),
]
