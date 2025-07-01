from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Site
from django.utils import timezone
from .permissions import SiteAccessPermission
import requests


class ConnectUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_id = request.data.get('id')
        access_key = request.data.get('access_key')
        if not user_id or not access_key:
            return Response({'error': 'user_id & access_key are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            site = Site.objects.get(access_key=access_key)
            if not site.is_active:
                return Response({'error': 'پشتیبانی این دامنه غیرفعال شده است.'}, status=status.HTTP_403_FORBIDDEN)
            if timezone.now() > site.expire_at:
                return Response({'error': 'پشتیبانی این سایت به پایان رسیده است.'}, status=status.HTTP_403_FORBIDDEN)
            if site.domain_owner_id:
                if user_id == site.domain_owner_id:
                    return Response({'error': 'این دامنه به اکانت شما متصل است.'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'error': 'این دامنه به اکانت دیگری متصل است.'}, status=status.HTTP_403_FORBIDDEN)
            site.domain_owner_id = user_id
            site.is_active = True
            site.save()
            return Response({'message': 'حساب شما به دامنه متصل شد.\n' + site.domain}, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            return Response({'error': 'کلید دسترسی معتبر نمی باشد.'}, status=status.HTTP_404_NOT_FOUND)


class DisconnectUser(APIView):
    permission_classes = (SiteAccessPermission,)

    def delete(self, request):
        site = request.site
        site.domain_owner_id = ''
        site.save()
        return Response({'message': 'حساب شما از دامنه جدا شد.\n' + site.domain}, status=status.HTTP_200_OK)


class ServerAvailable(APIView):
    permission_classes = (SiteAccessPermission,)

    def get(self, request):
        site = request.site
        response = requests.get(f'{site.domain}/support/available/')
        if response.status_code == 200:
            return Response({'message': 'سرور فعال است.'}, status=status.HTTP_200_OK)
        return Response({'message': 'سرور غیر فعال است.'})


class ServerLoad(APIView):
    permission_classes = (SiteAccessPermission,)

    def get(self, request):
        site = request.site
        response = requests.get(f'{site.domain}/support/server_load/')
        if response.status_code == 200:
            data = response.json()
            return Response({'cpu': data.get('cpu'), 'memory': data.get('memory'), 'disk': data.get('disk')}, status=status.HTTP_200_OK)
        return Response({'error': 'اتصال با سرور برقرار نشد.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ServerBackup(APIView):
    permission_classes = (SiteAccessPermission,)

    def get(self, request):
        site = request.site
        response = requests.get(f'{site.domain}/support/backup/')
        if response.status_code == 200:
            return Response(response.content, status=status.HTTP_200_OK)
        return Response({'error': 'اتصال با سرور برقرار نشد.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


