from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    confirmation_code = models.CharField(max_length=6)
    def __str__(self):
        return self.username

class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field = models.CharField(max_length=255)
    qualifications = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
class Hirer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=255)

class Gig(models.Model):
    user = models.ForeignKey(Hirer, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    gig_description = models.CharField(max_length=255)
    gig_requirements = models.TextField()

class Bid(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    message = models.TextField()

class Post(models.Model):
    user = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    image = CloudinaryField('image', folder='jobBoard', blank=True, null=True)
    