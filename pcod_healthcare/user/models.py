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


class Comminityjoin(models.Model):
    userid=models.IntegerField()
    comminityid=models.IntegerField()
    a_status=models.IntegerField()


class Communitychatbox(models.Model):
    userid=models.IntegerField()
    comminityid=models.IntegerField()
    message=models.TextField(max_length=30)
    a_status=models.IntegerField()
    
