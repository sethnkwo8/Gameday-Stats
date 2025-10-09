from django.http import HttpResponse, request
from django.shortcuts import render
from .models import League, Team

import requests

teams = Team.objects.all()

for team in teams:
    print(team.api_id)

url = "https://v3.football.api-sports.io/players/squads?team=33"

payload={}
headers = {
  'x-rapidapi-key': 'b964567100c98e72c1d982378ead8833',
  'x-rapidapi-host': 'v3.football.api-sports.io'
}

response = requests.request("GET", url, headers=headers, data=payload)

players = response.json()["response"][0]["players"]

# for player in players:
#     print(player["name"])

# Create your views here.
def index(request):
    return render(request, "football/index.html")