# Generated by Django 3.2.8 on 2021-12-07 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('p18website', '0002_auto_20211207_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='ID',
        ),
    ]
