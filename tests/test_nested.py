
from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .forms import TestForm
from .utils import TemplateTestMixin, template_dirs


@template_dirs('nested_tag')
class TestNestedTag(TemplateTestMixin, SimpleTestCase):

    def setUp(self):
        super(TestNestedTag, self).setUp()
        self.ctx['form'] = TestForm()

    def test_invalid_noarg(self):
        with self.assertRaises(TemplateSyntaxError):
            get_template('invalid')

    def test_invalid_twoarg(self):
        with self.assertRaises(TemplateSyntaxError):
            get_template('invalid2')

    def test_empty_nest(self):
        tmpl = get_template('empty')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, '<fieldset><caption></caption></fieldset>\n')

    def test_simple(self):
        tmpl = get_template('simple')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, '<fieldset><caption>Caption</caption>content goes here</fieldset>\n')

    def test_asvar(self):
        tmpl = get_template('asvar')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, '\nBEFORE <fieldset><caption>Caption</caption>content goes here</fieldset>\n')

    def test_nested_content_still_has_parent_widgets(self):
        tmpl = get_template('keep_widgets')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, '\n<fieldset><caption></caption><input type="text" name="" value=""></fieldset>\n')
