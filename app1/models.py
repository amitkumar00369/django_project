from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password
class StudentModel(models.Model):
    
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=10)
    mobileNo=models.CharField(max_length=15)
    countryCode=models.CharField(max_length=3)
    countryName=models.CharField(max_length=50)
    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
class tokenModel(models.Model):
    token=models.CharField(max_length=255)
    userId=models.IntegerField()
    email=models.EmailField(max_length=50)
    