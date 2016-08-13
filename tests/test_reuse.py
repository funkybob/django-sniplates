
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin, template_dirs


@template_dirs('reuse')
class TestReuse(TemplateTestMixin, SimpleTestCase):

    def test_reuse(self):
        tmpl = get_template('reuse')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'true\n')

    def _test_simple(self):
        '''
        Using reuse in a base template can't work.

        It would require we construct a BlockContext, but we have no access to
        the template root node.
        '''
        tmpl = get_template('simple')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, '\ntrue\ntrue\n')

    def test_reuse_in_widget(self):
        '''
        Widget templates want to reuse their own blocks.
        '''
        tmpl = get_template('inwidget')
        try:
            tmpl.render(self.ctx)
        except:
            self.fail('{% reuse %} failure')
