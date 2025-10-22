import requests
from django.core.management.base import BaseCommand
from football.models import League, Team

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}


class Command(BaseCommand):
    help = "Update coaches for all teams using Football-Data API"

    def handle(self, *args, **options):
        leagues = League.objects.exclude(api_id_football_data__isnull=True)

        if not leagues.exists():
            self.stdout.write(self.style.WARNING("⚠️ No leagues found with Football-Data API IDs."))
            return

        for league in leagues:
            url = f"https://api.football-data.org/v4/competitions/{league.api_id_football_data}/teams"
            response = requests.get(url, headers=HEADERS)

            if response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to fetch teams for {league.name}: {response.text}")
                )
                continue

            data = response.json()
            teams = data.get("teams", [])
            updated_count = 0

            for t in teams:
                api_id = t.get("id")
                team_obj = Team.objects.filter(api_id_football_data=api_id).first()

                if not team_obj:
                    continue

                # Extract coach info if available
                coach_info = t.get("coach")
                if coach_info and coach_info.get("name"):
                    coach_name = coach_info.get("name")
                else:
                    coach_name = None

                if coach_name and coach_name != team_obj.coach_name:
                    team_obj.coach_name = coach_name
                    team_obj.save(update_fields=["coach_name"])
                    updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(f"✅ Updated {updated_count} coaches for teams in {league.name}")
            )