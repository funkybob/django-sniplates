
from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin


class TestReuse(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'base': '''{% block main %}{% endblock %}''',
        'reuse': '''{% extends 'base' %}{% load sniplates %}{% block true %}true{% endblock %}{% block main %}{% reuse 'true' %}{% endblock %}''',
    }

    def test_reuse(self):
        tmpl = get_template('reuse')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'true')
