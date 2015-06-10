
from django import forms


class TestForm(forms.Form):
    char = forms.CharField()
    oneof = forms.ChoiceField(choices=tuple(enumerate('abcd')))
    # empty value must be empty string, not string 'None'
    hidden_oneof = forms.ChoiceField(
        choices=tuple(enumerate('abcd')), required=False,
        widget=forms.HiddenInput, initial=None
    )
