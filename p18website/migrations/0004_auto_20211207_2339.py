# Generated by Django 3.2.8 on 2021-12-07 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('p18website', '0003_remove_package_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='JSProgram',
        ),
        migrations.RemoveField(
            model_name='package',
            name='content',
        ),
    ]
