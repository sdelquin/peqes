from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name
