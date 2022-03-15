from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(unique= True , max_length=50)
    password = models.CharField(max_length= 50)
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField()
    verified = models.BooleanField(null = False)