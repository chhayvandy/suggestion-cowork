from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

class Suggestion(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    longtitude = models.CharField(max_length=100, blank=True, default='')
    latitude   = models.CharField(max_length=100, blank=True, default='')
    class Meta:
        ordering = ('created',)