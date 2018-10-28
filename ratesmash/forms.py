from django import forms


class RoomForm(forms.Form):
    SERVER_LIST = (
            ('tetsu', 'tetsu_server'),
            ('kaillera', 'kaillera_server'),
            ('exo', 'exo_server'),
            )
    server = forms.ChoiceField(choices=SERVER_LIST)
    CF_LIST = (
            ('1', '1'),
            ('2', '2'),
            )
    cf = forms.ChoiceField(choices=CF_LIST)
    comment = forms.CharField(max_length=20, required=False)
    
    
class ResultForm(forms.Form):
    WINLOSS = (
            (True, 'win'),
            (False, 'loss')
            )
    result = forms.ChoiceField(choices=WINLOSS, widget=forms.RadioSelect())