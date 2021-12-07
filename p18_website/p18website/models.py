from django.db import models

class Package(models.Model):
    name = models.CharField(max_length = 200, blank=True, default='')
    version = models.CharField(max_length = 200, blank=True, default='')
    ID = models.CharField(max_length = 200, blank=True, default='')