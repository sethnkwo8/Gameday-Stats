import json
from django.core.management.base import BaseCommand
from ...models import League, Team, Player, Match, Standings, Top_Scorers

class Command(BaseCommand):
    help = "Load all data from data.json into the database"

    def handle(self, *args, **kwargs):
        file_path = "data.json"  # data.json should be in the same directory as manage.py

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # --- LEAGUES ---
        for item in data.get("leagues", []):
            League.objects.update_or_create(
                api_id_football_data=item.get("api_id_football_data"),
                defaults={
                    "name": item.get("name"),
                    "country": item.get("country"),
                    "season": item.get("season"),
                    "current_matchday": item.get("current_matchday"),
                    "total_matchdays": item.get("total_matchdays")
                }
            )
        self.stdout.write(self.style.SUCCESS("Leagues loaded"))

        # --- TEAMS ---
        for item in data.get("teams", []):
            league = League.objects.get(api_id_football_data=item["league_api_id"])
            Team.objects.update_or_create(
                api_id_football_data=item.get("api_id_football_data"),
                defaults={
                    "api_id_football_api": item.get("api_id_football_api"),
                    "abbreviation": item.get("abbreviation"),
                    "name": item.get("name"),
                    "league": league,
                    "logo": item.get("logo"),
                    "coach_name": item.get("coach_name"),
                    "venue": item.get("venue"),
                    "founded": item.get("founded"),
                    "website": item.get("website"),
                    "club_colors": item.get("club_colors")
                }
            )
        self.stdout.write(self.style.SUCCESS("Teams loaded"))

        # --- PLAYERS ---
        for item in data.get("players", []):
            team = Team.objects.get(api_id_football_data=item["team_api_id"])
            Player.objects.update_or_create(
                api_id_football_data=item.get("api_id_football_data"),
                defaults={
                    "name": item.get("name"),
                    "position": item.get("position"),
                    "team": team,
                    "age": item.get("age"),
                    "number": item.get("number"),
                    "photo": item.get("photo")
                }
            )
        self.stdout.write(self.style.SUCCESS("Players loaded"))

        # --- MATCHES ---
        for item in data.get("matches", []):
            league = League.objects.get(api_id_football_data=item["league_api_id"])
            home = Team.objects.get(api_id_football_data=item["home_api_id"])
            away = Team.objects.get(api_id_football_data=item["away_api_id"])
            Match.objects.update_or_create(
                api_id=item.get("api_id"),
                defaults={
                    "matchday": item.get("matchday"),
                    "league": league,
                    "home": home,
                    "away": away,
                    "date": item.get("date"),
                    "home_score": item.get("home_score"),
                    "away_score": item.get("away_score"),
                    "status": item.get("status"),
                    "referee": item.get("referee")
                }
            )
        self.stdout.write(self.style.SUCCESS("Matches loaded"))

        # --- STANDINGS ---
        for item in data.get("standings", []):
            league = League.objects.get(api_id_football_data=item["league_api_id"])
            team = Team.objects.get(api_id_football_data=item["team_api_id"])
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
                    "goalDifference": item.get("goalDifference")
                }
            )
        self.stdout.write(self.style.SUCCESS("Standings loaded"))

        # --- TOP SCORERS ---
        for item in data.get("top_scorers", []):
            league = League.objects.get(api_id_football_data=item["league_api_id"])
            player = Player.objects.get(api_id_football_data=item["player_api_id"])
            Top_Scorers.objects.update_or_create(
                league=league,
                player=player,
                defaults={
                    "goals": item.get("goals", 0),
                    "assists": item.get("assists", 0),
                    "penalties": item.get("penalties", 0)
                }
            )
        self.stdout.write(self.style.SUCCESS("Top scorers loaded"))

        self.stdout.write(self.style.SUCCESS("All data loaded successfully!"))