from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Site
from SupportBotAPI.utilities import to_jalali_verbose


admin.site.unregister(Group)
admin.site.unregister(User)

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain_owner', 'domain', 'get_created_at', 'get_expire_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'expire_at')
    list_editable = ('is_active',)
    search_fields = ('domain', 'domain_owner')
    ordering = ('-created_at',)


    def get_expire_at(self, obj):
        return to_jalali_verbose(obj.expire_at)
    get_expire_at.short_description = 'Expiration date'


    def get_created_at(self, obj):
        return to_jalali_verbose(obj.created_at)
    get_created_at.short_description = 'Creation date'
