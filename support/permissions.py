from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.conf import settings


class AccessDenied(PermissionDenied):
    default_detail = 'Access Denied'
    default_code = 'access_denied'
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE



class HasSupportAccess(BasePermission):
    def has_permission(self, request, view):
        if not settings.ENABLE_SUPPORT:
            raise AccessDenied()

        access_key = request.data.get('access_key') or request.query_params.get('access_key')

        if access_key != settings.SUPPORT_ACCESS_KEY:
            raise AccessDenied()

        return True

