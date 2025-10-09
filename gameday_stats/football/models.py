from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    season = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Team(models.Model):
    api_id = models.CharField(max_length=3, unique=True)
    abbreviation = models.CharField(max_length=4, blank=True)
    name = models.CharField(max_length=30)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league')
    logo = models.ImageField(blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=15, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team")
    age = models.IntegerField(max_length=3, null=True)
    number = models.IntegerField(max_length=3, null=True)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Finished", "Finished"),
        ("Live", "Live")
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_played")
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home")
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away")
    date = models.DateField()
    time = models.TimeField()
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Upcoming")
    last_updated = models.DateTimeField(auto_now=True)

class Player_Stats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="match")
    goals = models.IntegerField()
    assists = models.IntegerField()
    saves = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()