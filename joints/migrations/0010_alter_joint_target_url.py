# Generated by Django 5.1.4 on 2025-03-10 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joints', '0009_alter_joint_custom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joint',
            name='target_url',
            field=models.URLField(max_length=2048, unique=True),
        ),
    ]
