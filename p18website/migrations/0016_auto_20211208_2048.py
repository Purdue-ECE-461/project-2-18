# Generated by Django 3.2.8 on 2021-12-08 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('p18website', '0015_auto_20211208_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='highlighted',
        ),
        migrations.RemoveField(
            model_name='package',
            name='owner',
        ),
    ]
