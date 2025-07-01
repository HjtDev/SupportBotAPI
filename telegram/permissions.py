from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Site


class SiteDoesNotExist(PermissionDenied):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'هیچ دامنه ای به حساب شما متصل نیست.'
    default_code = 'site_not_found'


class SiteNotActive(PermissionDenied):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'پشتیبانی این دامنه غیر فعال شده است.'
    default_code = 'site_not_active'


class SiteSupportExpired(PermissionDenied):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'پشتیبانی این سایت به پایان رسیده است.'
    default_code = 'site_expired'


class UserIDNotProvided(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'id is required.'
    default_code = 'user_id_not_provided'


class SiteAccessPermission(BasePermission):
    def has_permission(self, request, view):
        user_id = request.data.get('id') or request.query_params.get('id')
        if not user_id:
            raise UserIDNotProvided()
        try:
            site = Site.objects.get(domain_owner_id=user_id)
        except Site.DoesNotExist:
            raise SiteDoesNotExist()
        if not site.is_active:
            raise SiteNotActive()
        if timezone.now() > site.expire_at:
            raise SiteSupportExpired()

        request.site = site
        request.user_id = user_id
        return True