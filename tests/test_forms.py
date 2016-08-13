
from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .forms import TestForm
from .utils import TemplateTestMixin, template_dirs


@template_dirs('field_tag')
class TestFieldTag(TemplateTestMixin, SimpleTestCase):

    def setUp(self):
        super(TestFieldTag, self).setUp()
        self.ctx['form'] = TestForm()

    def test_field_tag(self):
        '''
        Make sure the field tag is usable.
        '''
        tmpl = get_template('field')
        tmpl.render(self.ctx)

    def test_choices_field(self):
        tmpl = get_template('choices')
        output = tmpl.render(self.ctx)

        self.assertTrue('<option value="0">a</option>' in output)

    def test_choices_display(self):
        tmpl = get_template('choices')
        self.ctx['form'] = TestForm(initial={'oneof': 2})
        output = tmpl.render(self.ctx)

        self.assertTrue('Selected: c' in output)

    def test_choices_multi(self):
        tmpl = get_template('choices_multi')
        selected = [1, 3]
        self.ctx['form'] = TestForm(initial={'many': selected})
        output = tmpl.render(self.ctx)

        for idx, opt in enumerate('abcd'):
            self.assertTrue('<option value="{}" {}>{}'.format(
                idx,
                'selected' if idx in selected else '',
                opt,
            ) in output)

    def test_choices_multi2(self):
        """
        Edge case where one choice value is a substring of another choice value.
        """

        tmpl = get_template('choices_multi2')
        selected = [11, 22]
        self.ctx['form'] = TestForm(initial={'many2': selected})
        output = tmpl.render(self.ctx)

        for idx, opt in ((1, 'a'), (11, 'b'), (22, 'c')):
            expected = '<option value="{}" {}>{}'.format(
                idx,
                'selected' if idx in selected else '',
                opt,
            )
            self.assertTrue(expected in output, 'Expected %s' % expected)

    def test_widget_override(self):
        tmpl = get_template('override')
        output = tmpl.render(self.ctx)

        self.assertTrue('type="password"' in output)

    def test_widget_override2(self):
        tmpl = get_template('override2')
        output = tmpl.render(self.ctx)

        self.assertTrue('type="dummy"' in output)

    def test_empty_fiend(self):
        tmpl = get_template('empty_field')
        with self.assertRaises(TemplateSyntaxError):
            output = tmpl.render(self.ctx)
