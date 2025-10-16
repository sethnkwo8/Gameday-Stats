from django import forms
from .models import League, Match


class LeagueForm(forms.Form):
    leagues = forms.ModelChoiceField(queryset=League.objects.all(),
                                     label='',
                                     to_field_name='api_id_football_data',
                                      widget=forms.Select(attrs={'class':"form-select form-select-lg mb-3 ", "id":"league_select"}))
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["leagues"].empty_label = 'Choose a league'

class MatchdayForm(forms.Form):
    matchdays = forms.ChoiceField(
        label="Matchdays",
        widget=forms.Select(attrs={
            'class': "form-select form-select-lg mb-3",
            'id': "matchday_select"
        })
    )

    def __init__(self, *args, **kwargs):
        league = kwargs.pop("league", None)
        super().__init__(*args, **kwargs)

        queryset = Match.objects.all()
        if league:
            queryset = queryset.filter(league=league)

        matchdays = queryset.values_list('matchday', flat=True).distinct().order_by('matchday')
        self.fields['matchdays'].choices = [(md, f"Matchday {md}") for md in matchdays if md is not None]