from django.db import models


class Server(models.Model):
    site_access = models.BooleanField(default=True, verbose_name='Site Access')

    def __str__(self):
        return f'Server Status: {self.site_access}'

    class Meta:
        verbose_name = 'Server'
