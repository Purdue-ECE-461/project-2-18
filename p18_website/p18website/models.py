from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class Package(models.Model):
    name = models.CharField(max_length=200, blank=True, default='')
    version = models.CharField(max_length=200, blank=True, default='')
    url = models.CharField(max_length=200, blank=True, default='')
    content = models.CharField(max_length=10000, blank=True, default='')
    JSProgram = models.CharField(max_length=200, blank=True, default='')
    # owner = models.ForeignKey('auth.User', related_name='package', on_delete=models.CASCADE, null=True)
    # highlighted = models.TextField(null=True)

    # def save(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     self.highlighted = highlight(self.name, self.version)
    #     super().save(*args, **kwargs)
