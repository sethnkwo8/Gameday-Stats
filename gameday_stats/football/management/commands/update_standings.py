import os
import requests
from django.core.management.base import BaseCommand
from ...models import League, Team, Standings  # adjust import to your app name


class Command(BaseCommand):
    help = "Fetch and update Premier League standings from Football-Data API"

    def handle(self, *args, **options):
        api_token = os.getenv("FOOTBALL_DATA_API_KEY")  # API token from env
        url = "https://api.football-data.org/v4/competitions/2015/standings"

        headers = {"X-Auth-Token": api_token}

        # Fetch data from API
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"API Error: {response.status_code} - {response.text}"))
            return

        data = response.json()
        league_name = data["competition"]["name"]
        league_id = data["competition"]["id"]

        # Get league object
        try:
            league = League.objects.get(api_id_football_data=league_id)
        except League.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"League '{league_name}' not found in DB"))
            return

        self.stdout.write(self.style.SUCCESS(f"Updating standings for {league_name}"))

        # Loop through standings table
        for standings in data["standings"]:
            if standings["type"] != "TOTAL":
                continue  # Skip home/away splits

            for entry in standings["table"]:
                team_data = entry["team"]

                try:
                    team = Team.objects.get(name__iexact=team_data["name"])
                except Team.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Skipping unknown team: {team_data['name']}"))
                    continue

                Standings.objects.update_or_create(
                    league=league,
                    team=team,
                    defaults={
                        "position": entry["position"],
                        "played": entry["playedGames"],
                        "wins": entry["won"],
                        "draws": entry["draw"],
                        "lost": entry["lost"],
                        "points": entry["points"],
                        "goalsFor": entry["goalsFor"],
                        "goalsAgainst": entry["goalsAgainst"],
                        "goalDifference": entry["goalDifference"],
                    }
                )

                self.stdout.write(self.style.SUCCESS(f"Updated: {team.name} ({entry['points']} pts)"))

        self.stdout.write(self.style.SUCCESS("✅ Standings update complete!"))