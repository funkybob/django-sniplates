
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin, template_path, override_settings


@override_settings(
    TEMPLATE_DIRS=[template_path('inheritance')],
)
class TestInheritanceTag(TemplateTestMixin, SimpleTestCase):

    def test_block_super(self):
        tmpl = get_template('super')
        self.ctx.push({'widget_template': "super_widget_inherit"})
        output = tmpl.render(self.ctx)
        self.ctx.pop()
        self.assertEqual(output, 'EXTENDING BASE')

    def test_inherited_referenced_directly(self):
        tmpl = get_template('super')
        self.ctx.push({'widget_template': "super_widget_base"})
        output = tmpl.render(self.ctx)
        self.ctx.pop()
        self.assertEqual(output, 'BASE')
