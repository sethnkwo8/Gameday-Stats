import requests
from django.core.management.base import BaseCommand
from football.models import League, Player, Top_Scorers

import os
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}


class Command(BaseCommand):
    help = "Fetch and update top scorers for all leagues that have an api_id_football_data"

    def handle(self, *args, **options):
        leagues = League.objects.exclude(api_id_football_data__isnull=True)

        if not leagues.exists():
            self.stdout.write(self.style.WARNING("⚠️ No leagues with Football-Data API IDs found."))
            return

        for league in leagues:
            url = f"https://api.football-data.org/v4/competitions/{league.api_id_football_data}/scorers"
            response = requests.get(url, headers=HEADERS)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"❌ Failed to fetch scorers for {league.name}: {response.text}"))
                continue

            data = response.json()
            scorers = data.get("scorers", [])

            if not scorers:
                self.stdout.write(self.style.WARNING(f"⚠️ No scorers returned for {league.name}."))
                continue

            for scorer in scorers:
                player_data = scorer.get("player", {})
                team_data = scorer.get("team", {})

                player_name = player_data.get("name", "")
                goals = scorer.get("goals", 0)
                assists = scorer.get("assists", 0)
                penalties = scorer.get("penalties", 0)

                # Try to find player by full name
                player, created = Player.objects.get_or_create(
                    name=player_name,
                    defaults={"team": None}
                )

                # Update or create top scorer entry
                Top_Scorers.objects.update_or_create(
                    league=league,
                    player=player,
                    defaults={
                        "goals": goals,
                        "assists": assists,
                        "penalties": penalties,
                    },
                )

                action = "Created" if created else "Updated"
                self.stdout.write(f"{action} top scorer entry for {player_name} in {league.name}")

            self.stdout.write(self.style.SUCCESS(f"✅ Finished updating top scorers for {league.name}"))

        self.stdout.write(self.style.SUCCESS("🏁 All top scorers updated successfully!"))