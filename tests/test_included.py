
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin, template_dirs


@template_dirs('include')
class TestIncluded(TemplateTestMixin, SimpleTestCase):

    def test_include_with_soft(self):
        tmpl = get_template('base')
        output = tmpl.render(self.ctx)
        self.assertEqual(output.strip(), 'FOO')
