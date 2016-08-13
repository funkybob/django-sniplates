
from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin, template_dirs


@template_dirs('load_widgets')
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


@template_dirs('invalid')
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


@template_dirs('widget_tag')
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

    def test_asvar(self):
        tmpl = get_template('asvar')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'AFTER fixed')

    def test_empty_alias_reference(self):
        tmpl = get_template('alias_self')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'referenced referencing')
