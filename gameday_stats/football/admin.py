from django.contrib import admin
from .models import League, Team, Player, Match, Player_Stats

class LeagueModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'season')

class TeamModelAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'name', 'league', 'api_id')

# Register your models here.
admin.site.register(League, LeagueModelAdmin)
admin.site.register(Team, TeamModelAdmin)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Player_Stats)
