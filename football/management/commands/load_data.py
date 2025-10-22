import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from football.models import League, Team, Player, Match, Standings, Top_Scorers

class Command(BaseCommand):
    help = 'Load entire data.json into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading data from data.json...')
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # --- LEAGUES ---
        league_data = data.get("leagues", [])
        for item in league_data:
            league, _ = League.objects.update_or_create(
                api_id_football_data=item.get("api_id_football_data"),
                defaults={
                    "name": item.get("name"),
                    "country": item.get("country"),
                    "season": item.get("season"),
                    "current_matchday": item.get("current_matchday"),
                    "total_matchdays": item.get("total_matchdays"),
                }
            )

        # --- TEAMS ---
        team_data = data.get("teams", [])
        for item in team_data:
            league = League.objects.filter(api_id_football_data=item.get("league_id")).first()
            if not league:
                continue
            Team.objects.update_or_create(
                api_id_football_data=item.get("api_id_football_data"),
                defaults={
                    "api_id_football_api": item.get("api_id_football_api"),
                    "name": item.get("name"),
                    "abbreviation": item.get("abbreviation"),
                    "league": league,
                    "logo": item.get("logo"),
                    "coach_name": item.get("coach_name"),
                    "venue": item.get("venue"),
                    "founded": item.get("founded"),
                    "website": item.get("website"),
                    "club_colors": item.get("club_colors"),
                }
            )

        # --- PLAYERS ---
        player_data = data.get("players", [])
        for item in player_data:
            team = Team.objects.filter(api_id_football_data=item.get("team_id")).first()
            if not team:
                continue
            Player.objects.update_or_create(
                api_id_football_data=item.get("api_id_football_data"),
                defaults={
                    "name": item.get("name"),
                    "position": item.get("position"),
                    "team": team,
                    "age": item.get("age"),
                    "number": item.get("number"),
                    "photo": item.get("photo"),
                }
            )

        # --- MATCHES ---
        match_data = data.get("matches", [])
        for item in match_data:
            league = League.objects.filter(api_id_football_data=item.get("league_id")).first()
            home_team = Team.objects.filter(api_id_football_data=item.get("home_id")).first()
            away_team = Team.objects.filter(api_id_football_data=item.get("away_id")).first()
            if not league or not home_team or not away_team:
                continue
            Match.objects.update_or_create(
                api_id=item.get("api_id"),
                defaults={
                    "league": league,
                    "matchday": item.get("matchday"),
                    "home": home_team,
                    "away": away_team,
                    "date": parse_datetime(item.get("date")),
                    "home_score": item.get("home_score"),
                    "away_score": item.get("away_score"),
                    "status": item.get("status"),
                    "referee": item.get("referee"),
                }
            )

        # --- STANDINGS ---
        standings_data = data.get("standings", [])
        for item in standings_data:
            league = League.objects.filter(api_id_football_data=item.get("league_id")).first()
            team = Team.objects.filter(api_id_football_data=item.get("team_id")).first()
            if not league or not team:
                continue
            Standings.objects.update_or_create(
                league=league,
                team=team,
                defaults={
                    "position": item.get("position"),
                    "played": item.get("played"),
                    "wins": item.get("wins"),
                    "draws": item.get("draws"),
                    "lost": item.get("lost"),
                    "points": item.get("points"),
                    "goalsFor": item.get("goalsFor"),
                    "goalsAgainst": item.get("goalsAgainst"),
                    "goalDifference": item.get("goalDifference"),
                }
            )

        # --- TOP SCORERS ---
        scorers_data = data.get("top_scorers", [])
        for item in scorers_data:
            league = League.objects.filter(api_id_football_data=item.get("league_id")).first()
            player = Player.objects.filter(api_id_football_data=item.get("player_id")).first()
            if not league or not player:
                continue
            Top_Scorers.objects.update_or_create(
                league=league,
                player=player,
                defaults={
                    "goals": item.get("goals", 0),
                    "assists": item.get("assists", 0),
                    "penalties": item.get("penalties", 0),
                }
            )

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))