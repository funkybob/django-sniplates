
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin


class TestFieldTag(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'field': '{% load sniplates %}{% form_field form.field %}'
    }

    def test_field_tag(self):
        '''
        Make sure the field tag is usable.
        '''
        tmpl = get_template('field')
        output = tmpl.render(self.ctx)
