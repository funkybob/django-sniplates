
from django import forms


class TestForm(forms.Form):
    char = forms.CharField()
    oneof = forms.ChoiceField(choices=tuple(enumerate('abcd')))
    many = forms.MultipleChoiceField(choices=tuple(enumerate('abcd')))
    many2 = forms.MultipleChoiceField(choices=((1, 'a'), (11, 'b'), (22, 'c')))
