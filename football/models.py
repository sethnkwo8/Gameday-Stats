from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    api_id_football_data = models.IntegerField(unique=True, null=True)
    current_matchday = models.IntegerField(null=True)
    total_matchdays = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    api_id_football_api = models.IntegerField(unique=True, null=True)
    api_id_football_data = models.IntegerField(unique=True, null=True)
    abbreviation = models.CharField(max_length=4, blank=True, null=True)
    name = models.CharField(max_length=30)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league')
    logo = models.URLField(null=True)
    coach_name = models.CharField(max_length=100, blank=True, null=True)
    venue = models.CharField(max_length=100, blank=True, null=True)
    founded = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    club_colors = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=30, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team")
    age = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    photo = models.URLField( null=True)
    api_id_football_data = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("In Play", "In Play"),
        ("Finished", "Finished"),
        ("Postponed", "Postponed"),
        ("Canceled", "Canceled")
    ]

    matchday = models.IntegerField(null=True)
    api_id = models.IntegerField(unique=True, null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_played")
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home")
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away")
    date = models.DateTimeField()
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")
    referee = models.CharField(max_length=60, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Matchday {self.matchday} - {self.home.name} ({self.home_score}) v ({self.away_score}) {self.away.name} ({self.league.name})"
    
    class Meta:
        ordering = ["-date"]

class Top_Scorers(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_top_scorer", null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player")
    goals = models.IntegerField(default=0, null=True)
    assists = models.IntegerField(default=0, null=True, blank=True)
    penalties = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.player.name} - {self.goals} goals, {self.assists} assists, {self.penalties} penalties"
    
    class Meta:
        ordering = ["league", "-goals"]

class Standings(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_standing")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_standing")
    position = models.IntegerField()
    played = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    lost = models.IntegerField()
    points = models.IntegerField()
    goalsFor = models.IntegerField()
    goalsAgainst = models.IntegerField()
    goalDifference = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

