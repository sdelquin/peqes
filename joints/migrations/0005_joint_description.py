# Generated by Django 5.1.4 on 2025-02-23 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joints', '0004_joint_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='joint',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
