from django.core.management.base import BaseCommand
from football.models import Team, Player
import os
import requests

class Command(BaseCommand):
    help = "Fetch all players for each team from API-Football and save to the database (skips teams with existing players)"

    def handle(self, *args, **kwargs):
        api_token = os.getenv("API_FOOTBALL_KEY") # API token from env
        teams = Team.objects.all()

        for team in teams:
            # ✅ Check if team already has players
            if Player.objects.filter(team=team).exists():
                self.stdout.write(self.style.SUCCESS(f"✅ Players already exist for {team.name}, skipping..."))
                continue

            self.stdout.write(self.style.NOTICE(f"Fetching players for {team.name}..."))

            url = f"https://v3.football.api-sports.io/players/squads?team={team.api_id_football_api}"

            headers = {
                'x-apisports-key': api_token
            }

            try:
                response = requests.get(url, headers=headers)
                data = response.json()

                # ⚠️ Handle missing or empty data
                if not data.get("response"):
                    self.stdout.write(self.style.WARNING(f"No players found for {team.name}."))
                    continue

                players = data["response"][0]["players"]

                for player in players:
                    Player.objects.update_or_create(
                        name=player["name"],
                        team=team,
                        defaults={
                            "position": player.get("position"),
                            "age": player.get("age"),
                            "number": player.get("number"),
                            "photo": player.get("photo")
                        }
                    )

                self.stdout.write(self.style.SUCCESS(f"✅ Saved players for {team.name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching {team.name}: {e}"))