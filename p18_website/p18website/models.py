from django.db import models

class Package(models.Model):
    name = models.CharField(blank=True, default='')
    version = models.CharField(blank=True, default='')
    ID = models.CharField(blank=True, default='')