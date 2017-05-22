
from django.template.loader import get_template
from django.test import SimpleTestCase

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from .utils import TemplateTestMixin, template_dirs


@template_dirs('include')
class TestIncluded(TemplateTestMixin, SimpleTestCase):

    def test_include_with_soft(self):
        tmpl = get_template('base')
        output = tmpl.render(self.ctx)
        self.assertEqual(output.strip(), 'FOO')

    @patch('sniplates.templatetags.sniplates.resolve_blocks')
    def test_ensure_soft_only_executes_once_on_include(self, resolve_blocks):
        tmpl = get_template('base')
        tmpl.render(self.ctx)
        self.assertEqual(resolve_blocks.call_count, 1)
