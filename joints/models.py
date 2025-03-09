import re
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.db.utils import IntegrityError

from . import utils


class Joint(models.Model):
    target_url = models.URLField(unique=True)
    shorten_url = models.CharField(unique=True, max_length=256)
    hits = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('tags.Tag', related_name='joints', blank=True)
    custom = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=['target_url', 'shorten_url'])]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.shorten_url:
            if not self.is_url(self.shorten_url):
                self.shorten_url = self.urlify(self.shorten_url)
            self.shorten_url = self.shorten_url.lower().rstrip('/')
            super().save(*args, **kwargs)
        else:
            # Generate a random shorten url
            while True:
                try:
                    self.shorten_url = self.urlify(utils.base36_uuid())
                    self.custom = False
                    super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    continue

    def __str__(self):
        return self.shorten_url

    @staticmethod
    def is_url(guess_url: str) -> bool:
        return re.fullmatch(r'^https?.*$', guess_url) is not None

    @staticmethod
    def urlify(path: str, base_url: str = settings.SHORTEN_BASE_URL) -> str:
        return urljoin(base_url, path)

    @property
    def shorten_path(self) -> str:
        return f'/{self.shorten_url.split("/")[-1]}'
