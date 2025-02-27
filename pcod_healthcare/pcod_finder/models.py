from django.db import models

# Create your models here.
class Usertable(models.Model):
    name=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    phoneno=models.CharField(max_length=30)
    dob=models.CharField(max_length=30)
    gender=models.CharField(max_length=30)
    password=models.CharField(max_length=30)

class PCOSPrediction(models.Model):
    cycle_length = models.FloatField()
    FSH = models.FloatField()
    LH = models.FloatField()
    FSH_LH = models.FloatField()
    waist_hip_ratio = models.FloatField()
    TSH = models.FloatField()
    AMH = models.FloatField()
    Vit_D3 = models.FloatField()
    PRG = models.FloatField()
    RBS = models.FloatField()
    weight_gain = models.IntegerField()
    hair_growth = models.IntegerField()
    skin_darkening = models.IntegerField()
    hair_loss = models.IntegerField()
    pimples = models.IntegerField()
    follicle_L = models.IntegerField()
    follicle_R = models.IntegerField()
    avg_f_size_L = models.FloatField()
    avg_f_size_R = models.FloatField()
    prediction_result = models.CharField(max_length=20)  # Store result
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for record creation

    def __str__(self):
        return f"PCOS Prediction ID {self.id} - {self.created_at}"