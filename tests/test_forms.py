
from django.template.loader import get_template
from django.test import SimpleTestCase

from .forms import TestForm
from .utils import TemplateTestMixin


class TestFieldTag(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'widgets': '''
            {% block CharField %}<input type="text" name="{{ html_name }}" value="{{ value|default:'' }}>{% endblock %}
            {% block ChoiceField %}<select name="{{ html_name }}" data-choices="{{ choices }}">{% for val, display in choices %}
                <option value="{{ val }}">{{ display }}</option>{% endfor %}
            </select>{% endblock %}
        ''',
        'widget2': '''
            {% block CharField %}<input type="dummy" name="{{ html_name }}" value="{{ value|default:'' }}>{% endblock %}
            {% block password %}<input type="password" name="{{ html_name }}" value="{{ value|default:'' }}>{% endblock %}
        ''',
        'field': '''{% load sniplates %}{% load_widgets form="widgets" %}{% form_field form.char %}''',
        'choices': '''{% load sniplates %}{% load_widgets form="widgets" %}{% form_field form.oneof %}''',
        'override': '''{% load sniplates %}{% load_widgets form="widgets" other="widget2" %}{% form_field form.char widget="other:password" %}''',
        'override2': '''{% load sniplates %}{% load_widgets form="widgets" other="widget2" %}{% form_field form.char alias="other" %}''',
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

    def test_widget_override(self):
        tmpl = get_template('override')
        output = tmpl.render(self.ctx)

        self.assertTrue('type="password"' in output)

        tmpl = get_template('override2')
        output = tmpl.render(self.ctx)

        self.assertTrue('type="dummy"' in output)
