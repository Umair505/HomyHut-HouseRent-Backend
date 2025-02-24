from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='account')
    profile_image = models.TextField(blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} Account'