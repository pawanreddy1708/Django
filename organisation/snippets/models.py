from django.db import models
from datetime import datetime
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=1024)
    age= models.IntegerField()
    designation = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.now())

    def __str__(self):
        print(self.name)