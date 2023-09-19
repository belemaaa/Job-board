from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Freelancer)
admin.site.register(models.Hirer)
admin.site.register(models.Gig)
admin.site.register(models.Bid)
admin.site.register(models.Post)
admin.site.register(models.SavedGigs)