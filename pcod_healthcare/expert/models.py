from django.db import models

# Create your models here.



class Community(models.Model):
    userid=models.TextField(max_length=10)
    name=models.TextField(max_length=90)
    description=models.TextField(max_length=90)
    Type=models.TextField(max_length=10)
    Rules=models.TextField(max_length=100)
    status=models.TextField(max_length=8)
    date_c=models.DateField(auto_now=True)

