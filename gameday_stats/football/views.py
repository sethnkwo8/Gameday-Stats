from django.http import HttpResponse, request, JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import LeagueForm
from .models import League, Team, Player, Standings

import requests

# Create your views here.
def index(request):
    form = LeagueForm()

    return render(request, "football/index.html", {
        "form":form
    })

def standings(request, league_id):
    selected_league = get_object_or_404(League, api_id_football_data=league_id)
    standings = Standings.objects.filter(league=selected_league).order_by('position')

    data = []
    for s in standings:
        data.append({
            "position": s.position,
            "name": s.team.name,
            "logo":s.team.logo,
            "played":s.played,
            "wins":s.wins,
            "draws":s.draws,
            "lost":s.lost,
            "goalsFor":s.goalsFor,
            "goalsAgainst":s.goalsAgainst,
            "goalDifference":s.goalDifference,
            "points":s.points
        })

    return JsonResponse({"standings":data})