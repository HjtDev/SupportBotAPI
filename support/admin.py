from django.contrib import admin
from django.shortcuts import redirect
from .models import Server
from django.utils.translation import gettext_lazy as _


@admin.register(Server)
class SettingAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Site Access'), {
            'fields': ['site_access'],
            'classes': ['collapse', 'tab-site-access'],
        })
    ]

    def has_add_permission(self, request):
        Server.objects.count()
        if Server.objects.count() == 0:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        qs = Server.objects.all()
        if qs.count() == 1:
            server = qs.first()
            return redirect(f'/admin/support/server/{server.pk}/change/')
        return super().changelist_view(request, extra_context)

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        if Server.objects.count() == 1:
            perms['add'] = False
        return perms
