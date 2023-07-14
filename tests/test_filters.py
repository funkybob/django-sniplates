from collections import OrderedDict

from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin, template_dirs


@template_dirs('filters')
class TestFilters(TemplateTestMixin, SimpleTestCase):

    def test_flatattrs(self):
        tmpl = get_template('flatattrs')
        self.ctx['a_dict'] = OrderedDict([
            ('a', 'aye'),
            ('b', 'bee'),
            ('c', 'cee'),
        ])
        output = tmpl.render(self.ctx)

        self.assertEqual(output, ' a="aye" b="bee" c="cee" \n')
