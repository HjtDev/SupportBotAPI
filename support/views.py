from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import psutil


class AvailableAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class ServerLoadAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
        }, status=status.HTTP_200_OK)
