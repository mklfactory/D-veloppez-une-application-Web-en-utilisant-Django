from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    image = models.ImageField(null=True, blank=True, upload_to='tickets/')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (par {self.user.username})"


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]  # 0 à 5

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline} — {self.rating}/5 (par {self.user.username})"


class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('user', 'followed_user')  # pas de doublon

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"