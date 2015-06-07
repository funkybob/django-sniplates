from django.test import SimpleTestCase
from django.template.loader import get_template
from .utils import TemplateTestMixin, template_path, override_settings

@override_settings(
    TEMPLATE_DIRS=[template_path('filters')],
)
class TestFilters(TemplateTestMixin, SimpleTestCase):

    def test_flatattrs(self):
        tmpl = get_template('flatattrs')
        self.ctx['a_dict'] = {
            'a': 'aye',
            'b': 'bee',
            'c': 'cee',
        }
        output = tmpl.render(self.ctx)

        self.assertEqual(output, ' a="aye" b="bee" c="cee" \n')
