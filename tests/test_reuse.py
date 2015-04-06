
from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin, template_path, override_settings

@override_settings(
    TEMPLATE_DIRS=[template_path('reuse')],
)
class TestReuse(TemplateTestMixin, SimpleTestCase):

    def test_reuse(self):
        tmpl = get_template('reuse')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'true\n')
