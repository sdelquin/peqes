# Generated by Django 5.1.4 on 2024-12-30 17:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='joint',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='joint',
            name='ttl',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Time to live (hours)', null=True),
        ),
        migrations.AddField(
            model_name='joint',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
