from django.contrib import admin
from .models import League, Team, Player, Match, Top_Scorers

class LeagueModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'season')

class TeamModelAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'name', 'league')

class PlayerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'team')

# Register your models here.
admin.site.register(League, LeagueModelAdmin)
admin.site.register(Team, TeamModelAdmin)
admin.site.register(Player, PlayerModelAdmin)
admin.site.register(Match)
admin.site.register(Top_Scorers)
