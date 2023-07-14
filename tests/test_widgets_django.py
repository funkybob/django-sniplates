"""
Tests for all shipped sniplates/django.html widgets.
"""
import datetime

import django
from django import forms
from django.template.loader import get_template
from django.test import SimpleTestCase
from django.utils.datastructures import MultiValueDict

from .forms import DjangoWidgetsForm, FilesForm
from .utils import TemplateTestMixin, template_dirs


class FakeFieldFile(object):
    """
    Quacks like a FieldFile (has a .url and unicode representation), but
    doesn't require us to care about storages etc.

    Taken from django.tests.forms_tests.test.test_widgets.
    """
    url = 'something'

    def __str__(self):
        return self.url


@template_dirs('field_tag')
class TestFieldTag(TemplateTestMixin, SimpleTestCase):

    def test_widgets_unbound(self):
        """
        Tests all form fields one by one, with a fresh, unbound form without
        initial data.
        """
        self.ctx['form'] = DjangoWidgetsForm()
        tmpl = get_template('widgets_django')
        output = tmpl.render(self.ctx)

        # map field to expected widget output
        expected_output = {
            'char': '<input type="text" name="char" id="id_char" value="" class=" " required>',
            'email': {
                '<3.2.20': '<input type="email" name="email" id="id_email" value="" class=" " required>',
                '>=3.2.20': '<input type="email" name="email" id="id_email" value="" class=" " maxlength="320" required>',
            },
            'url': '<input type="url" name="url" id="id_url" value="" class=" " required>',
            'number': '<input type="number" name="number" id="id_number" value="" class=" " required>',
            'password': '<input type="password" name="password" id="id_password" value="" class=" " required>',
            'hidden': '<input type="hidden" name="hidden" id="id_hidden" value="" class=" " required>',
            # this one is hard to test, as it may NOT contain the output - it's empty by default
            'multiple_hidden': [
                '<input type="hidden" name="multiple_hidden" id="id_multiple_hidden_0" value="N" required>',
                '<input type="hidden" name="multiple_hidden" id="id_multiple_hidden_1" value="o" required>',
                '<input type="hidden" name="multiple_hidden" id="id_multiple_hidden_2" value="n" required>',
                '<input type="hidden" name="multiple_hidden" id="id_multiple_hidden_3" value="e" required>',
            ],
            'date': '<input type="text" name="date" id="id_date" value="" class=" " required>',
            'datetime': '<input type="text" name="datetime" id="id_datetime" value="" class=" " required>',
            'time': '<input type="text" name="time" id="id_time" value="" class=" " required>',
            'text': '<textarea name="text" id="id_text" class=" " required cols="40" rows="10"></textarea> ',
            'checkbox': '''
                <label for="id_checkbox" class="">
                    <input name="checkbox" id="id_checkbox" type="checkbox">
                    Checkbox
                </label>''',
            'select': '''
                <select name="select" id="id_select">
                <option value="1">a</option>
                <option value="11">b</option>
                <option value="22">c</option>
                </select>''',
            'optgroup_select': '''
                <select id="id_optgroup_select" name="optgroup_select">
                    <optgroup label="label1">
                        <option value="1">a</option>
                        <option value="11">b</option>
                    </optgroup>
                    <optgroup label="label2">
                        <option value="22">c</option>
                    </optgroup>
                </select>''',
            'null_boolean_select': '''
                <select id="id_null_boolean_select" name="null_boolean_select">
                <option value="unknown" selected>Unknown</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
                </select>''',
            'select_multiple': '''
                <select name="select_multiple" id="id_select_multiple" multiple>
                    <option value="1">a</option>
                    <option value="11">b</option>
                    <option value="22">c</option>
                </select>''',
            'radio_select': '''
                <ul id="id_radio_select">
                    <li><input name="radio_select" type="radio" id="id_radio_select_0" value="1" >a</li>
                    <li><input name="radio_select" type="radio" id="id_radio_select_1" value="11" >b</li>
                    <li><input name="radio_select" type="radio" id="id_radio_select_2" value="22" >c</li>
                </ul>''',
            'checkbox_select_multiple': '''
                <ul id="id_checkbox_select_multiple">
                    <li><input name="checkbox_select_multiple" type="checkbox"
                        id="id_checkbox_select_multiple_0" value="1">a</li>
                    <li><input name="checkbox_select_multiple" type="checkbox"
                        id="id_checkbox_select_multiple_1" value="11">b</li>
                    <li><input name="checkbox_select_multiple" type="checkbox"
                        id="id_checkbox_select_multiple_2" value="22">c</li>
                </ul>''',
            'file': '<input id="id_file" name="file" type="file" value="" class=" " required>',
            'clearable_file': '''
                <input id="id_clearable_file" name="clearable_file" type="file" value="" class=" " required>''',
        }

        self.assertInHTML(expected_output['char'], output, msg_prefix='TextInput rendered incorrectly: ')
        if django.VERSION < (3, 2, 20):
            self.assertInHTML(expected_output['email']['<3.2.20'], output, msg_prefix='EmailInput rendered incorrectly: ')
        else:
            self.assertInHTML(expected_output['email']['>=3.2.20'], output, msg_prefix='EmailInput rendered incorrectly: ')
        self.assertInHTML(expected_output['url'], output, msg_prefix='UrlInput rendered incorrectly: ')
        self.assertInHTML(expected_output['number'], output, msg_prefix='NumberInput rendered incorrectly: ')
        self.assertInHTML(expected_output['password'], output, msg_prefix='PasswordInput rendered incorrectly: ')
        self.assertInHTML(expected_output['hidden'], output, msg_prefix='HiddenInput rendered incorrectly: ')

        for input_ in expected_output['multiple_hidden']:
            self.assertNotInHTML(input_, output, msg_prefix='MultipleHiddenInput rendered incorrectly: %s: ' % input_)
        self.assertInHTML(expected_output['date'], output, msg_prefix='DateInput rendered incorrectly: ')
        self.assertInHTML(expected_output['datetime'], output, msg_prefix='DateTimeInput rendered incorrectly: ')
        self.assertInHTML(expected_output['time'], output, msg_prefix='TimeInput rendered incorrectly: ')
        self.assertInHTML(expected_output['text'], output, msg_prefix='Textarea rendered incorrectly: ')
        self.assertInHTML(expected_output['checkbox'], output, msg_prefix='CheckboxInput rendered incorrectly: ')

        # all kind of selects
        self.assertInHTML(expected_output['select'], output, msg_prefix='Select rendered incorrectly: ')
        self.assertInHTML(
            expected_output['optgroup_select'], output, msg_prefix='Select with optgroups rendered incorrectly: ')
        self.assertInHTML(
            expected_output['null_boolean_select'], output, msg_prefix='NullBooleanSelect rendered incorrectly: ')
        self.assertInHTML(
            expected_output['select_multiple'], output, msg_prefix='SelectMultiple rendered incorrectly: ')
        self.assertInHTML(expected_output['radio_select'], output, msg_prefix='RadioSelect rendered incorrectly: ')
        self.assertInHTML(
            expected_output['checkbox_select_multiple'], output,
            msg_prefix='CheckboxSelectMultiple rendered incorrectly: '
        )
        self.assertInHTML(expected_output['file'], output, msg_prefix='FileInput rendered incorrectly: ')

    def test_widgets_bound(self):
        """
        Tests all form fields one by one, with a bound form.
        """
        self.ctx['form'] = DjangoWidgetsForm(data=MultiValueDict({
            'char': ['test char'],
            'email': ['foo@bar.com'],
            'url': ['https://example.com'],
            'number': [42],
            'password': ['secret'],
            'hidden': ['peek-a-boo'],
            'multiple_hidden': ['first', 'second'],
            'date': [datetime.date(2016, 1, 25)],
            'datetime': [datetime.datetime(2016, 1, 25, 9, 0, 42)],
            'time': [datetime.time(8, 9)],
            'text': ['Lorem ipsum...'],
            'checkbox': [True],
            'select': ['22'],
            'optgroup_select': ['22'],
            'null_boolean_select': ["false"],
            'select_multiple': ['11', '22', 1],
            'radio_select': ['11'],
            'checkbox_select_multiple': ['1', 11],
            'file': ['not-a-suspicious-file.exe'],
            'clearable_file': ['also-not-a-suspicious-file.exe'],
        }))
        tmpl = get_template('widgets_django')
        output = tmpl.render(self.ctx)

        expected = {
            'char': '<input type="text" name="char" id="id_char" value="test char" class=" " required>',
            'email': {
                '<3.2.20': '<input type="email" name="email" id="id_email" value="foo@bar.com" class=" " required>',
                '>=3.2.20': '<input type="email" name="email" id="id_email" value="foo@bar.com" class=" " maxlength="320" required>',
            },
            'url': '<input type="url" name="url" id="id_url" value="https://example.com" class=" " required>',
            'number': '<input type="number" name="number" id="id_number" value="42" class=" " required>',
            # Password inputs should not re-render their contents.
            'password': '<input type="password" name="password" id="id_password" value="" class=" " required>',
            'hidden': '<input type="hidden" name="hidden" id="id_hidden" value="peek-a-boo" class=" " required>',
            'multiple_hidden': [
                '<input type="hidden" name="multiple_hidden" id="id_multiple_hidden_0" value="first" required>',
                '<input type="hidden" name="multiple_hidden" id="id_multiple_hidden_1" value="second" required>',
            ],
            'date': '<input type="text" name="date" id="id_date" value="2016-01-25" class=" " required>',
            'datetime': '<input type="text" name="datetime" id="id_datetime" value="2016-01-25 09:00:42" class=" " required>',
            'time': '<input type="text" name="time" id="id_time" value="08:09:00" class=" " required>',
            'text': '<textarea name="text" id="id_text" class=" " required cols="40" rows="10">Lorem ipsum...</textarea> ',
            'checkbox': '''
                <label for="id_checkbox" class="">
                    <input name="checkbox" id="id_checkbox" type="checkbox" checked>
                    Checkbox
                </label>''',
            'select': '''
                <select name="select" id="id_select">
                <option value="1">a</option>
                <option value="11">b</option>
                <option value="22" selected>c</option>
                </select>''',
            'optgroup_select': '''
                <select id="id_optgroup_select" name="optgroup_select">
                    <optgroup label="label1">
                        <option value="1">a</option>
                        <option value="11">b</option>
                    </optgroup>
                    <optgroup label="label2">
                        <option value="22" selected>c</option>
                    </optgroup>
                </select>''',
            'null_boolean_select': '''
                <select id="id_null_boolean_select" name="null_boolean_select">
                    <option value="unknown">Unknown</option>
                    <option value="true">Yes</option>
                    <option value="false" selected>No</option>
                </select>''',
            'select_multiple': '''
                <select name="select_multiple" id="id_select_multiple" multiple>
                    <option value="1" selected>a</option>
                    <option value="11" selected>b</option>
                    <option value="22" selected>c</option>
                </select>''',
            'radio_select': '''
                <ul id="id_radio_select">
                    <li><input name="radio_select" type="radio" id="id_radio_select_0" value="1" >a</li>
                    <li><input name="radio_select" type="radio" id="id_radio_select_1" value="11" checked>b</li>
                    <li><input name="radio_select" type="radio" id="id_radio_select_2" value="22" >c</li>
                </ul>''',
            'checkbox_select_multiple': '''
                <ul id="id_checkbox_select_multiple">
                    <li><input name="checkbox_select_multiple" type="checkbox"
                        id="id_checkbox_select_multiple_0" value="1" checked>a</li>
                    <li><input name="checkbox_select_multiple" type="checkbox"
                        id="id_checkbox_select_multiple_1" value="11" checked>b</li>
                    <li><input name="checkbox_select_multiple" type="checkbox"
                        id="id_checkbox_select_multiple_2" value="22">c</li>
                </ul>''',
            # file inputs never show the value, the old value is of no use [see django.forms tests]
            'file': '<input id="id_file" name="file" type="file" value="" class=" error" required>',
            'clearable_file': '''
                <input id="id_clearable_file" name="clearable_file" type="file" value="" class=" error" required>''',
        }

        self.assertInHTML(expected['char'], output)
        if django.VERSION < (3, 2, 20):
            self.assertInHTML(expected['email']['<3.2.20'], output)
        else:
            self.assertInHTML(expected['email']['>=3.2.20'], output)
        self.assertInHTML(expected['url'], output)
        self.assertInHTML(expected['number'], output)
        self.assertInHTML(expected['password'], output)
        self.assertInHTML(expected['hidden'], output)
        for input_ in expected['multiple_hidden']:
            self.assertInHTML(input_, output)
        self.assertInHTML(expected['text'], output)
        self.assertInHTML(expected['checkbox'], output)

        self.assertInHTML(expected['select'], output)
        self.assertInHTML(expected['optgroup_select'], output)
        self.assertInHTML(expected['null_boolean_select'], output)
        self.assertInHTML(expected['select_multiple'], output)
        self.assertInHTML(expected['radio_select'], output)
        self.assertInHTML(expected['checkbox_select_multiple'], output)
        self.assertInHTML(expected['file'], output)
        self.assertInHTML(expected['clearable_file'], output)

        # DateTime based
        self.assertInHTML(expected['date'], output)
        self.assertInHTML(expected['datetime'], output)
        self.assertInHTML(expected['time'], output)

    def test_date_input_different_format(self):
        """
        Tests that the ``django.forms`` configured input format is respected.
        """
        class Form(forms.Form):
            date = forms.DateField(widget=forms.DateInput(format='%m-%Y-%d'))

        self.ctx['form'] = Form(initial={'date': datetime.date(2016, 3, 27)})
        tmpl = get_template('widgets_django')
        output = tmpl.render(self.ctx)
        self.assertHTMLEqual(
            output,
            '<input type="text" name="date" id="id_date" value="03-2016-27" class=" " required>'
        )

    def test_filefield_extractor(self):
        """
        Assert that the clearable file input is properly rendered.
        """
        self.ctx['form'] = FilesForm(initial={'clearable_file': FakeFieldFile()})
        tmpl = get_template('widgets_django')
        output = tmpl.render(self.ctx)
        self.assertHTMLEqual(
            output, '''
            Currently: <a href="something">something</a>
            <input type="checkbox" name="clearable_file-clear" id="clearable_file-clear_id" />
            <label for="clearable_file-clear_id">Clear</label><br />
            Change: <input id="id_clearable_file" name="clearable_file" type="file" class=" " value="" required />
            '''
        )
