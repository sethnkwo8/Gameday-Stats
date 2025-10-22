import requests
from django.core.management.base import BaseCommand
from football.models import League, Match, Team

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}


class Command(BaseCommand):
    help = "Update match scores and status for ongoing or finished matches from Football-Data API"

    def handle(self, *args, **options):
        leagues = League.objects.exclude(api_id_football_data__isnull=True)

        if not leagues.exists():
            self.stdout.write(self.style.WARNING("⚠️ No leagues with Football-Data API IDs found."))
            return

        for league in leagues:
            url = f"https://api.football-data.org/v4/competitions/{league.api_id_football_data}/matches"
            response = requests.get(url, headers=HEADERS)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"❌ Failed to fetch matches for {league.name}: {response.text}"))
                continue

            matches = response.json().get("matches", [])

            updated_count = 0

            for m in matches:
                status = m.get("status")
                if status not in ["IN_PLAY", "FINISHED"]:
                    continue  # skip scheduled, postponed, canceled, etc.

                api_id = m.get("id")
                match_obj = Match.objects.filter(api_id=api_id).first()

                if not match_obj:
                    continue  # skip if match not found locally

                match_obj.home_score = m.get("score", {}).get("fullTime", {}).get("home")
                match_obj.away_score = m.get("score", {}).get("fullTime", {}).get("away")
                match_obj.status = status.replace("_", " ").title()
                match_obj.referee = (
                    m.get("referees")[0]["name"]
                    if m.get("referees") and len(m.get("referees")) > 0
                    else match_obj.referee
                )
                match_obj.save(update_fields=["home_score", "away_score", "status", "referee", "last_updated"])

                updated_count += 1

            self.stdout.write(self.style.SUCCESS(f"🏁 Updated {updated_count} matches for {league.name}"))