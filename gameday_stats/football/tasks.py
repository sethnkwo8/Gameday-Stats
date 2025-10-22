from celery import shared_task
from django.core.management import call_command

@shared_task
def update_coaches_task():
    call_command('update_coaches')

@shared_task
def update_current_matchday_task():
    call_command('update_current_matchday')

@shared_task
def update_matches_task():
    call_command('update_matches')

@shared_task
def update_players_task():
    call_command('update_players')

@shared_task
def update_standings_task():
    call_command('update_standings')

@shared_task
def update_top_scorers_task():
    call_command('update_top_scorers')