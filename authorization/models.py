from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return self.username

