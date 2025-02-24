from django.db import models
from django.contrib.auth.models import User
from rent.models import RentAdvertisement

class Review(models.Model):
    STAR_CHOICES = [
        ('⭐', '⭐'),
        ('⭐⭐', '⭐⭐'),
        ('⭐⭐⭐', '⭐⭐⭐'),
        ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
        ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    ad = models.ForeignKey(RentAdvertisement, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(choices=STAR_CHOICES, max_length=10)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'ad']

    def __str__(self):
        return f"{self.user.username} - {self.ad.title} ({self.rating})"