from rest_framework.serializers import ModelSerializer
from .models import Site
from SupportBotAPI.utilities import to_jalali_verbose


class SiteSerializer(ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = to_jalali_verbose(instance.created_at)
        rep['expire_at'] = to_jalali_verbose(instance.expire_at)
        return rep
