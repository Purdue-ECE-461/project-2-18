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
    owner = models.ForeignKey('auth.User', related_name='package', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)
