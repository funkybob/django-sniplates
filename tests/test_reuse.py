
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

    def test_simple(self):
        '''
        Widget templates want to reuse their own blocks.
        '''
        tmpl = get_template('simple')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, '\n\ntrue\n\ntrue\n')

    def test_reuse_in_widget(self):
        tmpl = get_template('inwidget')
        output = tmpl.render(self.ctx)
