import requests
from django.core.management.base import BaseCommand
from football.models import League, Team, Standings

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}


class Command(BaseCommand):
    help = "Fetch and update current standings for all leagues with Football-Data API IDs"

    def handle(self, *args, **options):
        leagues = League.objects.exclude(api_id_football_data__isnull=True)

        if not leagues.exists():
            self.stdout.write(self.style.WARNING("⚠️ No leagues with Football-Data API IDs found."))
            return

        for league in leagues:
            url = f"https://api.football-data.org/v4/competitions/{league.api_id_football_data}/standings"
            response = requests.get(url, headers=HEADERS)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"❌ Failed to fetch standings for {league.name}: {response.text}"))
                continue

            data = response.json()
            standings_list = data.get("standings", [])

            if not standings_list:
                self.stdout.write(self.style.WARNING(f"⚠️ No standings returned for {league.name}."))
                continue

            # Clear old standings for this league
            Standings.objects.filter(league=league).delete()

            # Usually the first item in standings[] is the "TOTAL" table
            for table in standings_list:
                if table.get("type") != "TOTAL":
                    continue

                for entry in table.get("table", []):
                    team_data = entry.get("team", {})
                    team_name = team_data.get("name", "")
                    api_team_id = team_data.get("id", None)

                    # Find team by name or Football-Data API ID
                    team = (
                        Team.objects.filter(api_id_football_data=api_team_id).first()
                        or Team.objects.filter(name__iexact=team_name).first()
                    )

                    if not team:
                        self.stdout.write(self.style.WARNING(f"⚠️ Team not found in DB: {team_name}"))
                        continue

                    Standings.objects.create(
                        league=league,
                        team=team,
                        position=entry.get("position", 0),
                        played=entry.get("playedGames", 0),
                        wins=entry.get("won", 0),
                        draws=entry.get("draw", 0),
                        lost=entry.get("lost", 0),
                        points=entry.get("points", 0),
                        goalsFor=entry.get("goalsFor", 0),
                        goalsAgainst=entry.get("goalsAgainst", 0),
                        goalDifference=entry.get("goalDifference", 0),
                    )

            self.stdout.write(self.style.SUCCESS(f"✅ Updated standings for {league.name}"))

        self.stdout.write(self.style.SUCCESS("🏁 All league standings updated successfully!"))