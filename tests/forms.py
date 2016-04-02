
from django import forms


class TestForm(forms.Form):
    char = forms.CharField()
    oneof = forms.ChoiceField(choices=tuple(enumerate('abcd')))
    many = forms.MultipleChoiceField(choices=tuple(enumerate('abcd')))
    many2 = forms.MultipleChoiceField(choices=((1, 'a'), (11, 'b'), (22, 'c')))


class DjangoWidgetsForm(forms.Form):
    char = forms.CharField()
    email = forms.EmailField()
    url = forms.URLField()
    number = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    hidden = forms.CharField(widget=forms.HiddenInput)
    multiple_hidden = forms.ChoiceField(choices=((1, 'a'), (11, 'b'), (22, 'c')),
                                        widget=forms.MultipleHiddenInput)
    date = forms.DateField()
    datetime = forms.DateTimeField()
    time = forms.TimeField()
    text = forms.CharField(widget=forms.Textarea)
    checkbox = forms.BooleanField()
    select = forms.ChoiceField(choices=((1, 'a'), (11, 'b'), (22, 'c')))
    optgroup_select = forms.ChoiceField(choices=(
        ('label1', [(1, 'a'), (11, 'b')]),
        ('label2', [(22, 'c')])
    ))
    null_boolean_select = forms.NullBooleanField()
    select_multiple = forms.MultipleChoiceField(choices=((1, 'a'), (11, 'b'), (22, 'c')))
    radio_select = forms.ChoiceField(choices=((1, 'a'), (11, 'b'), (22, 'c')),
                                     widget=forms.RadioSelect)
    checkbox_select_multiple = forms.MultipleChoiceField(
        choices=((1, 'a'), (11, 'b'), (22, 'c')),
        widget=forms.CheckboxSelectMultiple
    )

    file = forms.FileField(widget=forms.FileInput)
    clearable_file = forms.FileField()
    # TODO: clearableFileInput, FileInput, Split(Hidden)DateTimeWidget


class FilesForm(forms.Form):
    clearable_file = forms.FileField()
