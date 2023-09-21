from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    def __str__(self):
        return self.username

class ConfirmationCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    
class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field = models.CharField(max_length=255)
    qualifications = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
class Hirer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class Gig(models.Model):
    user = models.ForeignKey(Hirer, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    gig_description = models.CharField(max_length=255)
    gig_requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gig by {self.user.user.username} created at {self.created_at}"

class Bid(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.bidder.user.username} created at {self.created_at}"

class Post(models.Model):
    user = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    image = CloudinaryField('image', folder='jobBoard', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Post by {self.user.user.username} created at {self.created_at}"
    
class SavedGig(models.Model):
    user = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gig saved at {self.saved_at} by {self.user.user.username}"