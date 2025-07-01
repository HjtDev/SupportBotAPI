from django.db import models


class Site(models.Model):
    domain = models.URLField(blank=False, null=False, verbose_name='Site domain')
    access_key = models.CharField(blank=False, null=False, max_length=128)
    expire_at = models.DateTimeField(blank=False, null=False, verbose_name='Expire At')
    is_active = models.BooleanField(default=True, verbose_name='Is active')
    domain_owner = models.CharField(blank=True, null=True, max_length=255, verbose_name='Domain owner name')
    domain_owner_id = models.CharField(blank=True, null=True, max_length=255, verbose_name='Domain owner id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Started at')


    def __str__(self):
        return f'{self.domain_owner} - {self.domain}'

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'
