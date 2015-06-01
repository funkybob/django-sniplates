
from django.template.loader import get_template
from django.test import SimpleTestCase

from .forms import TestForm
from .utils import TemplateTestMixin, template_path, override_settings


@override_settings(
    TEMPLATE_DIRS=[template_path('field_tag')],
)
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

    def test_widget_override(self):
        tmpl = get_template('override')
        output = tmpl.render(self.ctx)

        self.assertTrue('type="password"' in output)

    def test_widget_override2(self):
        tmpl = get_template('override2')
        output = tmpl.render(self.ctx)

        self.assertTrue('type="dummy"' in output)

    def test_value_none(self):
        tmpl = get_template('choices_value_none')
        output = tmpl.render(self.ctx)

        self.assertTrue('value=""' in output)
        self.assertFalse('value="None"' in output)

    def test_display_multivalue(self):
        """
        Test that iterables as value don't break the 'display' computation.
        """
        tmpl = get_template('multiplechoice')
        output = tmpl.render(self.ctx)
        self.assertEqual(output, 'a, b\n')
