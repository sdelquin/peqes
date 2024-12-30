# Generated by Django 5.1.4 on 2024-12-30 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joints', '0003_remove_joint_ttl_joint_expires_at'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='joint',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='joints', to='tags.tag'),
        ),
    ]
