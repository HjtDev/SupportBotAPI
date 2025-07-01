from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework import status

from .models import Server


class SiteAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if '/api/v1/' in request.path:
            return None
        if '/support/' in request.path:
            return None
        return HttpResponse('سرور خاموش است.',
                        status=status.HTTP_403_FORBIDDEN) if not Server.objects.first().site_access else None
