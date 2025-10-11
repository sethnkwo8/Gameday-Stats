from django.http import HttpResponse, request
from django.shortcuts import render
from .forms import LeagueForm
from .models import League, Team, Player

import requests

# Create your views here.
def index(request):
    form = LeagueForm()
    return render(request, "football/index.html", {
        "form":form
    })
