
from django import forms
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin


class TestForm(forms.Form):
    char = forms.CharField()
    oneof = forms.ChoiceField(choices=tuple(enumerate('abcd')))


class TestFieldTag(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'widgets': '''
            {% block CharField %}<input type="text" name="{{ html_name }}" value="{{ value|default:'' }}>{% endblock %}
            {% block ChoiceField %}<select name="{{ html_name }}" data-choices="{{ choices }}">{% for val, display in choices %}
                <option value="{{ val }}">{{ display }}</option>{% endfor %}
            </select>{% endblock %}
        ''',
        'field': '''{% load sniplates %}{% load_widgets form="widgets" %}{% form_field form.char %}''',
        'choices': '''{% load sniplates %}{% load_widgets form="widgets" %}{% form_field form.oneof %}''',
    }
    def setUp(self):
        super(TestFieldTag, self).setUp()
        self.ctx['form'] = TestForm()

    def test_field_tag(self):
        '''
        Make sure the field tag is usable.
        '''
        tmpl = get_template('field')
        output = tmpl.render(self.ctx)

    def test_choices_field(self):
        tmpl = get_template('choices')
        output = tmpl.render(self.ctx)

        self.assertTrue('<option value="0">a</option>' in output)
