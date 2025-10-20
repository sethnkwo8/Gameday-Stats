from django.urls import path
from . import views

app_name = "football"

urlpatterns = [
    path("", views.index, name="index" ),
    path("<int:team_id>", views.teams_details, name="team_details"),

    # API Routes
    path("standings/<int:league_id>", views.standings, name="standings"),
    path("matchday/<int:league_id>/<int:matchday>", views.matchday, name="matchday"),
    path("teams/<int:league_id>", views.teams, name="teams"),
    path("top_scorers/<int:league_id>", views.top_scorers, name="top_scorers")
]