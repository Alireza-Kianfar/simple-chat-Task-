from django.conf import settings
from django.db import models
class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_user = models.BooleanField(default=True)