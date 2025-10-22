import requests
from django.core.management.base import BaseCommand
from football.models import Team, Player

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}


class Command(BaseCommand):
    help = "Update all team players (e.g., during transfer windows) using Football-Data API"

    def handle(self, *args, **options):
        teams = Team.objects.exclude(api_id_football_data__isnull=True)

        if not teams.exists():
            self.stdout.write(self.style.WARNING("⚠️ No teams found with Football-Data API IDs."))
            return

        for team in teams:
            url = f"https://api.football-data.org/v4/teams/{team.api_id_football_data}"
            response = requests.get(url, headers=HEADERS)

            if response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to fetch players for {team.name}: {response.text}")
                )
                continue

            data = response.json()
            squad = data.get("squad", [])

            if not squad:
                self.stdout.write(self.style.WARNING(f"⚠️ No players found for {team.name}"))
                continue

            existing_player_ids = set(
                Player.objects.filter(team=team).values_list("api_id_football_data", flat=True)
            )
            fetched_player_ids = set()

            for player_data in squad:
                player_id = player_data.get("id")
                fetched_player_ids.add(player_id)

                player, created = Player.objects.update_or_create(
                    api_id_football_data=player_id,
                    defaults={
                        "name": player_data.get("name"),
                        "position": player_data.get("position"),
                        "team": team,
                        "age": player_data.get("dateOfBirth") and 
                               (2025 - int(player_data["dateOfBirth"][:4])) if player_data.get("dateOfBirth") else None,
                        "number": player_data.get("shirtNumber"),
                        "photo": None,  
                    },
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"🟢 Added {player.name} to {team.name}"))
                else:
                    self.stdout.write(self.style.NOTICE(f"🟡 Updated {player.name} in {team.name}"))

            removed_players = existing_player_ids - fetched_player_ids
            if removed_players:
                Player.objects.filter(api_id_football_data__in=removed_players, team=team).delete()
                self.stdout.write(
                    self.style.WARNING(f"❌ Removed {len(removed_players)} player(s) no longer in {team.name}")
                )

            self.stdout.write(self.style.SUCCESS(f"✅ Finished updating {team.name}"))