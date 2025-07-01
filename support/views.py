from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from io import StringIO
from django.core.management import call_command
import psutil
from .permissions import HasSupportAccess
from .models import Server
from random import randint


class AvailableAPIView(APIView):
    permission_classes = [HasSupportAccess]

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK if Server.objects.first().site_access else status.HTTP_423_LOCKED)


class ServerLoadAPIView(APIView):
    permission_classes = [HasSupportAccess]

    def get(self, request, *args, **kwargs):
        return Response({
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
        }, status=status.HTTP_200_OK)


class ServerBackupAPIView(APIView):
    permission_classes = [HasSupportAccess]

    def get(self, request, *args, **kwargs):
        out = StringIO()
        call_command('dumpdata', stdout=out, indent=2)
        out.seek(0)
        json_data = out.read()

        json_bytes = json_data.encode('utf-8')

        response = HttpResponse(json_bytes, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="backup.json"'
        return response


class ServerOnAPIView(APIView):
    permission_classes = [HasSupportAccess]

    def get(self, request, *args, **kwargs):
        server = Server.objects.first()
        if not server.site_access:
            server.site_access = True
            server.save()
        return Response(status=status.HTTP_200_OK)


class ServerOffAPIView(APIView):
    permission_classes = [HasSupportAccess]

    def get(self, request, *args, **kwargs):
        server = Server.objects.first()
        if server.site_access:
            server.site_access = False
            server.save()
        return Response(status=status.HTTP_200_OK)


class ServerInfoAPIView(APIView):
    permission_classes = [HasSupportAccess]

    def get(self, request, *args, **kwargs):
        return Response({
            'فروش کل': randint(0, 1000),
            'فروش این ماه': randint(0, 1000),
            'بازدید های سایت': randint(0, 1000),
            'تعداد کاربران': randint(0, 1000),
            'پرفروش ترین محصول': randint(0, 1000),
            'تعداد کامنت های جدید': randint(0, 1000)
        }, status=status.HTTP_200_OK)
