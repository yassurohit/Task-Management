from django.db import models

from user.models import CustomUser

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100,unique=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='teams_created')
    members = models.ManyToManyField(CustomUser,related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
   

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
    )
    title = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=1000)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20,choices= STATUS_CHOICES,default = 'pending')
    assigned_to = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,related_name='assigned_tasks')
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='tasks')
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='comments')
    written_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
