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
            if timezone.now() > site.expire_at:
                return Response({'error': 'پشتیبانی این سایت به پایان رسیده است.'}, status=status.HTTP_403_FORBIDDEN)
            if site.is_active:  # taken
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
