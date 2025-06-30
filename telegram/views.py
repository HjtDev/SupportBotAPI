import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Site
from django.utils import timezone


class ConnectUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
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
            if site.domain_owner_id:  # taken
                if user_id == site.domain_owner_id:
                    return Response({'error': 'این دامنه به اکانت شما متصل است.'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'error': 'این دامنه به اکانت دیگری متصل است.'}, status=status.HTTP_403_FORBIDDEN)
            site.domain_owner_id = user_id
            site.is_active = True
            site.save()
            return Response({'message': 'حساب شما به دامنه متصل شد.' + f'\n{site.domain}'}, status=status.HTTP_200_OK)

        except Site.DoesNotExist:
            return Response({'error': 'کلید دسترسی معتبر نمی باشد.'}, status=status.HTTP_404_NOT_FOUND)


class DisconnectUser(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('id')

        try:
            site = Site.objects.get(domain_owner_id=user_id)
            if site.is_active:
                site.domain_owner_id = ''
                site.save()
                return Response({'message': 'حساب شما از دامنه جدا شد.' + f'\n{site.domain}'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'پشتیبانی این دامنه غیرفعال شده است.'}, status=status.HTTP_403_FORBIDDEN)
        except Site.DoesNotExist:
            return Response({'error': 'هیچ دامنه ای به حساب شما متصل نیست.'}, status=status.HTTP_404_NOT_FOUND)


class ServerAvailable(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        try:
            site = Site.objects.get(domain_owner_id=user_id)
            if site.is_active:
                response = requests.get(f'{site.domain}/support/available/')
                if response.status_code == 200:
                    return Response({'message': 'سرور فعال است.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'سرور غیر فعال است.'})
            else:
                return Response({'error': 'پشتیبانی این دامنه غیرفعال شده است.'}, status=status.HTTP_403_FORBIDDEN)
        except Site.DoesNotExist:
            return Response({'error': 'هیچ دامنه ای به حساب شما متصل نیست.'}, status=status.HTTP_404_NOT_FOUND)
