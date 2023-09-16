from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username
    
class Gig(models.Model):
    gig_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gig_name = models.CharField(max_length=255)
    gig_description = models.CharField(max_length=255)


class Job(models.Model):
    job_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=255)
    job_description = models.CharField(max_length=255)
    job_requirements = models.TextField()