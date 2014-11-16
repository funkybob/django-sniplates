
from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .forms import TestForm
from .utils import TemplateTestMixin


class TestNestedTag(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'widgets': '''
            {% block fieldset %}<fieldset><caption>{{ caption }}</caption>{{ content|safe }}</fieldset>{% endblock %}
            {% block CharField %}<input type="text" name="{{ html_name }}" value="{{ value|default:'' }}>{% endblock %}
            {% block ChoiceField %}<select name="{{ html_name }}" data-choices="{{ choices }}">{% for val, display in choices %}
                <option value="{{ val }}">{{ display }}</option>{% endfor %}
            </select>{% endblock %}
        ''',
        'invalid': '''{% load sniplates %}{% nested_widget %}''',
        'invalid2': '''{% load sniplates %}{% nested_widget 'foo:bar' baz %}''',
        'empty': '''{% load sniplates %}{% load_widgets form="widgets" %}{% nested_widget "form:fieldset" %}{% endnested %}''',
        'simple': '''{% load sniplates %}{% load_widgets form="widgets" %}{% nested_widget "form:fieldset" caption="Caption" %}content goes here{% endnested %}''',
    }
    def setUp(self):
        super(TestNestedTag, self).setUp()
        self.ctx['form'] = TestForm()

    def test_invalid_noarg(self):
        with self.assertRaises(TemplateSyntaxError):
            tmpl = get_template('invalid')

    def test_invalid_twoarg(self):
        with self.assertRaises(TemplateSyntaxError):
            tmpl = get_template('invalid2')

    def test_empty_nest(self):
        tmpl = get_template('empty')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, '<fieldset><caption></caption></fieldset>')

    def test_simple(self):
        tmpl = get_template('simple')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, '<fieldset><caption>Caption</caption>content goes here</fieldset>')

