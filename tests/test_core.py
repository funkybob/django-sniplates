
from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase, override_settings

from .utils import TemplateTestMixin, template_path


@override_settings(
    TEMPLATE_DIRS=[template_path('load_widgets')],
)
class TestLoadWidgets(TemplateTestMixin, SimpleTestCase):

    def test_load_widgets(self):
        tmpl = get_template('load_widgets')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'success\n')

    def test_load_widgets_two(self):
        tmpl = get_template('load_widgets_two')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'success<=>winning\n')

    def test_load_widgets_three(self):
        tmpl = get_template('load_widgets_three')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'success<=>winning\n')


@override_settings(
    TEMPLATE_DIRS=[template_path('invalid')],
)
class TestInvalid(TemplateTestMixin, SimpleTestCase):

    def test_bad_name(self):
        tmpl = get_template('bad_name')
        with self.assertRaises(TemplateSyntaxError):
            tmpl.render(self.ctx)

    def test_not_loaded(self):
        tmpl = get_template('not_loaded')
        with self.assertRaises(TemplateSyntaxError):
            tmpl.render(self.ctx)

    def test_no_lib(self):
        tmpl = get_template('no_lib')
        with self.assertRaises(TemplateSyntaxError):
            tmpl.render(self.ctx)

    def test_no_widget(self):
        tmpl = get_template('no_widget')
        with self.assertRaises(TemplateSyntaxError):
            tmpl.render(self.ctx)


@override_settings(
    TEMPLATE_DIRS=[template_path('widget_tag')],
)
class TestWidgetTag(TemplateTestMixin, SimpleTestCase):

    def test_fixed(self):
        tmpl = get_template('fixed')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'fixed\n')

    def test_var(self):
        tmpl = get_template('var')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'value\n')

    def test_inherit(self):
        tmpl = get_template('inherit')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'more value\n')


@override_settings(
    TEMPLATE_DIRS=[template_path('inheritance')],
)
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
