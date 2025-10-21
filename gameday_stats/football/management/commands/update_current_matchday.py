import requests
from django.core.management.base import BaseCommand
from football.models import League

import os

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}


class Command(BaseCommand):
    help = "Update the current matchday for all leagues using Football-Data API"

    def handle(self, *args, **options):
        leagues = League.objects.exclude(api_id_football_data__isnull=True)

        if not leagues.exists():
            self.stdout.write(self.style.WARNING("⚠️ No leagues found with Football-Data API IDs."))
            return

        for league in leagues:
            url = f"https://api.football-data.org/v4/competitions/{league.api_id_football_data}"
            response = requests.get(url, headers=HEADERS)

            if response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to fetch data for {league.name}: {response.text}")
                )
                continue

            data = response.json()
            current_season = data.get("currentSeason", {})
            current_matchday = current_season.get("currentMatchday")

            if current_matchday:
                league.current_matchday = current_matchday
                league.save(update_fields=["current_matchday"])
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ {league.name}: current matchday updated to {current_matchday}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ No matchday data available for {league.name}")
                )