from django.db import models
from django.utils import timezone

# Create your models here.


class Message(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
