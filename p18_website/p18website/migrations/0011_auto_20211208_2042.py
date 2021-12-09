# Generated by Django 3.2.8 on 2021-12-08 20:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('p18website', '0010_auto_20211208_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='highlighted',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='package',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='package', to=settings.AUTH_USER_MODEL),
        ),
    ]