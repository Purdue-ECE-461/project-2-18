from django.db import models

class Package(models.Model):
    name = models.CharField(max_length = 200, blank=True, default='')
    version = models.CharField(max_length = 200, blank=True, default='')
    url = models.CharField(max_length = 200, blank=True, default='')
    content = models.CharField(max_length = 1000, blank=True, default='')
    JSProgram = models.CharField(max_length = 200, blank=True, default='')
