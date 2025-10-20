from django.db.models import Q
from django.http import HttpResponse, request, JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import LeagueForm, MatchdayForm
from .models import League, Match, Player, Standings, Team, Top_Scorers

import requests

# Create your views here.
def index(request):
    default_league = League.objects.first()
    league_form = LeagueForm()

    if default_league:
        # Always pass the league to the form
        matchday_form = MatchdayForm(
            league=default_league,
            initial={
                "matchdays": default_league.current_matchday
            } if default_league.current_matchday else None
        )
    else:
        matchday_form = MatchdayForm()  # fallback if no leagues exist

    return render(request, "football/index.html", {
        "league_form": league_form,
        "matchday_form": matchday_form,
        "default_league": default_league
    })

def standings(request, league_id):
    selected_league = get_object_or_404(League, api_id_football_data=league_id)
    standings = Standings.objects.filter(league=selected_league).order_by('position')

    data = []
    for s in standings:
        data.append({
            "position": s.position,
            "team_id": s.team.pk,
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

def matchday(request, league_id, matchday):
    selected_league = get_object_or_404(League, api_id_football_data=league_id)
    matches = Match.objects.filter(league=selected_league, matchday=matchday).select_related("home", "away").order_by("date")

    data = []
    for m in matches:
        data.append({
            "date": m.date.strftime("%Y-%m-%d %H:%M"),
            "home":m.home.name,
            "home_logo":getattr(m.home, "logo", None),
            "home_score":m.home_score,
            "away": m.away.name,
            "away_logo":getattr(m.away, "logo", None),
            "away_score": m.away_score,
            "status": m.status,
            "referee":m.referee
        })

    return JsonResponse({"matches":data})

def teams(request, league_id):
    selected_league = get_object_or_404(League, api_id_football_data=league_id)
    league_teams = Team.objects.filter(league=selected_league).order_by("name")

    data = []
    for team in league_teams:
        data.append({
            "team_id":team.pk,
            "team_logo":team.logo,
            "team_name":team.name,
            "team_league": team.league.name,
            "team_coach":team.coach_name,
            "team_venue":team.venue
        })

    return JsonResponse({"teams": data})

def teams_details(request, team_id):
    selected_team = Team.objects.get(pk=team_id)
    team_matches = Match.objects.filter(
        Q(home=selected_team) | Q(away=selected_team)
    ).order_by('date')
    team_players = Player.objects.filter(team=selected_team).order_by('-photo').order_by('number')

    team_league_standings = Standings.objects.filter(league=selected_team.league).order_by('position')


    return render(request, "football/team_details.html", {
        "team":selected_team,
        "matches":team_matches,
        "players":team_players,
        "standings":team_league_standings
    })

def top_scorers(request, league_id):
    selected_league = League.objects.get(api_id_football_data = league_id)
    scorers = Top_Scorers.objects.filter(league=selected_league)

    data = []
    for scorer in scorers:
        data.append({
            "scorer_photo":scorer.player.photo,
            "scorer_team": scorer.player.team.name,
            "scorer_team_photo": scorer.player.team.logo,
            "scorer_name": scorer.player.name,
            "scorer_position": scorer.player.position,
            "scorer_goals": scorer.goals,
            "scorer_assists":scorer.assists,
            "scorer_penalties":scorer.penalties
        })

    return JsonResponse({"scorers": data})
