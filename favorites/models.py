from django.db import models
from django.contrib.auth.models import User
from rent.models import RentAdvertisement

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    ad = models.ForeignKey(RentAdvertisement, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'ad']

    def __str__(self):
        return f"{self.user.username} - {self.ad.title}"