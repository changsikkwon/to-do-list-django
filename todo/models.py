from django.db import models
from user.models import User
    
class Status(models.Model):
  status_name = models.CharField(max_length=32)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  class Meta:
    db_table = "status"
    
class ToDo(models.Model):
  title = models.CharField(max_length=32)
  content = models.TextField()
  status = models.ForeignKey(Status, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  
  class Meta:
    db_table = "to_do"