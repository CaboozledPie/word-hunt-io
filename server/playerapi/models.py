from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=50, unique=True)
    avatar_url = models.URLField(blank=True, null=True)

class LifetimeStats(models.Model):
    profile = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)

    # stats
    games_played = models.IntegerField(default=0)
    lifetime_score = models.BigIntegerField(default=0)
    biggest_word = models.CharField(max_length=50)
    unranked_wins = models.IntegerField(default=0)
    unranked_losses = models.IntegerField(default=0)
    ranked_wins = models.IntegerField(default=0)
    ranked_losses = models.IntegerField(default=0)
    
    words_found = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        default=list
    )

class AchievementData(models.Model):
    profile = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
