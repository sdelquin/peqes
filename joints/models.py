import datetime
import re
from urllib.parse import urljoin

from django.conf import settings
from django.db import models


class Joint(models.Model):
    target_url = models.URLField(unique=True)
    shorten_url = models.CharField(unique=True, max_length=256)
    hits = models.PositiveBigIntegerField(default=0)
    ttl = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text='Time to live (hours)', verbose_name='TTL'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['target_url', 'shorten_url'])]

    def save(self, *args, **kwargs):
        if not self.is_url(self.shorten_url):
            self.shorten_url = self.urlify(self.shorten_url)
        self.shorten_url = self.shorten_url.rstrip('/')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shorten_url

    @property
    def expires_at(self) -> datetime.datetime | None:
        if self.ttl:
            return self.created_at + datetime.timedelta(hours=self.ttl)
        return None

    @staticmethod
    def is_url(guess_url: str) -> bool:
        return re.fullmatch(r'^https?.*$', guess_url) is not None

    @staticmethod
    def urlify(path: str, base_url: str = settings.SHORTEN_BASE_URL) -> str:
        return urljoin(base_url, path)
