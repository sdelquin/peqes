# Generated by Django 5.1.4 on 2025-03-09 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joints', '0006_alter_joint_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='joint',
            name='custom',
            field=models.BooleanField(default=False),
        ),
    ]
