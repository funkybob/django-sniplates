
from django import forms
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin


class TestForm(forms.Form):
    char = forms.CharField()


class TestFieldTag(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'widgets': '''{% block CharField %}<input type="text" name="{{ name }}" value="{{ value|default:'' }}>{% endblock %}''',
        'field': '{% load sniplates %}{% load_widgets form="widgets" %}{% form_field form.char %}'
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
