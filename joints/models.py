import re
from urllib.parse import urljoin

from django.conf import settings
from django.db import models


class Joint(models.Model):
    target_url = models.URLField(unique=True)
    shorten_url = models.CharField(unique=True, max_length=256)
    hits = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField('tags.Tag', related_name='joints', blank=True)

    class Meta:
        indexes = [models.Index(fields=['target_url', 'shorten_url'])]

    def save(self, *args, **kwargs):
        if not self.is_url(self.shorten_url):
            self.shorten_url = self.urlify(self.shorten_url)
        self.shorten_url = self.shorten_url.rstrip('/')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shorten_url

    @staticmethod
    def is_url(guess_url: str) -> bool:
        return re.fullmatch(r'^https?.*$', guess_url) is not None

    @staticmethod
    def urlify(path: str, base_url: str = settings.SHORTEN_BASE_URL) -> str:
        return urljoin(base_url, path)
