from django.db import models

class User(models.Model):
  account = models.CharField(max_length=32)
  password = models.CharField(max_length=32)
  
  def __str__(self):
    return self.name