from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from io import StringIO
from django.core.management import call_command
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


class ServerBackupAPIView(APIView):
    def get(self, request, *args, **kwargs):
        out = StringIO()
        call_command('dumpdata', stdout=out, indent=2)
        out.seek(0)
        json_data = out.read()

        json_bytes = json_data.encode('utf-8')

        response = HttpResponse(json_bytes, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="backup.json"'
        return response
