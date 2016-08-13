from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin, template_dirs


@template_dirs('inheritance')
class TestInheritance(TemplateTestMixin, SimpleTestCase):

    def test_block_overlap(self):
        '''
        Ensure that when we reference a block from a sniplate that doesn't
        exist, but is in our template, it isn't used.
        '''
        tmpl = get_template('block_overlap')

        with self.assertRaises(TemplateSyntaxError):
            tmpl.render(self.ctx)

    def test_parent_inherit(self):
        '''
        When our parent template loads sniplates, we should have access to them
        also.
        '''
        tmpl = get_template('parent_inherit')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'foo\n')

    def test_parent_overlap(self):
        '''
        If a sniplate library has a block of the same name as in the calling
        template, we should NOT override it.
        '''
        tmpl = get_template('parent_overlap')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'first\n')

    def test_block_super(self):
        tmpl = get_template('super')
        self.ctx['widget_template'] = "super_widget_inherit"
        output = tmpl.render(self.ctx)
        self.assertEqual(output, 'EXTENDING BASE')

    def test_inherited_referenced_directly(self):
        tmpl = get_template('super')
        self.ctx['widget_template'] = "super_widget_base"
        output = tmpl.render(self.ctx)
        self.assertEqual(output, 'BASE')
