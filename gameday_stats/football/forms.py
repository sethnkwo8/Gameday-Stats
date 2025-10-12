from django import forms
from .models import League

class LeagueForm(forms.Form):
    leagues = forms.ModelChoiceField(queryset=League.objects.all(),
                                     label='',
                                     to_field_name='api_id_football_data',
                                      widget=forms.Select(attrs={'class':"form-select form-select-lg mb-3 ", "id":"league_select"}))
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["leagues"].empty_label = 'Choose a league'