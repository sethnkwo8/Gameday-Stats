from django.urls import path
from . import views

app_name = "football"

urlpatterns = [
    path("", views.index, name="index" ),

    # API Routes
    path("standings/<int:league_id>", views.standings, name="standings")
]