"""
Tests for all shipped sniplates/django.html widgets.
"""

from django.template.loader import get_template
from django.test import SimpleTestCase

from .forms import DjangoWidgetsForm
from .utils import TemplateTestMixin, template_path, override_settings


@override_settings(TEMPLATE_DIRS=[template_path('field_tag')])
class TestFieldTag(TemplateTestMixin, SimpleTestCase):

    def setUp(self):
        super(TestFieldTag, self).setUp()
        self.ctx['form'] = DjangoWidgetsForm()

    def test_widgets_unbound(self):
        """
        Tests all form fields one by one, with a fresh, unbound form without
        initial data.
        """
        tmpl = get_template('widgets_django')
        output = tmpl.render(self.ctx)

        # map field to expected widget output
        expected_output = {
            'char': '<input type="text" name="char" id="id_char" value="" class="" required>',
            'email': '<input type="email" name="email" id="id_email" value="" class="" required>',
            'url': '<input type="url" name="url" id="id_url" value="" class="" required>',
            'number': '<input type="number" name="number" id="id_number" value="" class="" required>',
            'password': '<input type="password" name="password" id="id_password" value="" class="" required>',
            'hidden': '<input type="hidden" name="hidden" id="id_hidden" value="" class="" required>',
            'multiple_hidden': '''
                <input type="hidden" name="multiple_hidden" id="id_multiple_hidden_0" value="" required>
                <input type="hidden" name="multiple_hidden" id="id_multiple_hidden_1" value="" required>
                <input type="hidden" name="multiple_hidden" id="id_multiple_hidden_2" value="" required>
                <input type="hidden" name="multiple_hidden" id="id_multiple_hidden_3" value="" required>''',
            'date': '<input type="date" name="date" id="id_date" value="" class="" required>',
            'datetime': '<input type="datetime" name="datetime" id="id_datetime" value="" class="" required>',
            'time': '<input type="time" name="time" id="id_time" value="" class="" required>',
            'text': '<textarea name="text" id="id_text" class="" required cols="40" rows="10"></textarea> ',
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
            'null_boolean_select': '''
                <select id="id_null_boolean_select" name="null_boolean_select">
                <option value="1" selected="selected">Unknown</option>
                <option value="2">Yes</option>
                <option value="3">No</option>
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
        }

        self.assertInHTML(expected_output['char'], output, msg_prefix='TextInput rendered incorrectly: ')
        self.assertInHTML(expected_output['email'], output, msg_prefix='EmailInput rendered incorrectly: ')
        self.assertInHTML(expected_output['url'], output, msg_prefix='UrlInput rendered incorrectly: ')
        self.assertInHTML(expected_output['number'], output, msg_prefix='NumberInput rendered incorrectly: ')
        self.assertInHTML(expected_output['password'], output, msg_prefix='PasswordInput rendered incorrectly: ')
        self.assertInHTML(expected_output['hidden'], output, msg_prefix='HiddenInput rendered incorrectly: ')

        self.assertInHTML(
            expected_output['multiple_hidden'], output, msg_prefix='MultipleHiddenInput rendered incorrectly: ')
        self.assertInHTML(expected_output['date'], output, msg_prefix='DateInput rendered incorrectly: ')
        self.assertInHTML(expected_output['datetime'], output, msg_prefix='DateTimeInput rendered incorrectly: ')
        self.assertInHTML(expected_output['time'], output, msg_prefix='TimeInput rendered incorrectly: ')
        self.assertInHTML(expected_output['text'], output, msg_prefix='Textarea rendered incorrectly: ')
        self.assertInHTML(expected_output['checkbox'], output, msg_prefix='CheckboxInput rendered incorrectly: ')

        # all kind of selects
        self.assertInHTML(expected_output['select'], output, msg_prefix='Select rendered incorrectly: ')
        self.assertInHTML(
            expected_output['null_boolean_select'], output, msg_prefix='NullBooleanSelect rendered incorrectly: ')
        self.assertInHTML(
            expected_output['select_multiple'], output, msg_prefix='SelectMultiple rendered incorrectly: ')
        self.assertInHTML(expected_output['radio_select'], output, msg_prefix='RadioSelect rendered incorrectly: ')
        self.assertInHTML(
            expected_output['checkbox_select_multiple'], output,
            msg_prefix='CheckboxSelectMultiple rendered incorrectly: '
        )
