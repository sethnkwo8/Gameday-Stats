from django.http import HttpResponse, request
from django.shortcuts import render
from .models import League, Team, Player

import requests

# Create your views here.
def index(request):
    return render(request, "football/index.html")