
from django import forms


class TestForm(forms.Form):
    char = forms.CharField()
    oneof = forms.ChoiceField(choices=tuple(enumerate('abcd')))
