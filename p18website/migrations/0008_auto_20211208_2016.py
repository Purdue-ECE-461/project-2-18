# Generated by Django 3.2.8 on 2021-12-08 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('p18website', '0007_auto_20211207_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='highlighted',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='package',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='package', to=settings.AUTH_USER_MODEL),
        ),
    ]
