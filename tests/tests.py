
from django.template import Context
from django.template.loader import get_template
from django.test.utils import setup_test_template_loader, restore_template_loaders
from django.test import SimpleTestCase

from sniplates.templatetags.sniplates import WIDGET_CONTEXT_KEY


class TemplateTestMixin(object):
    TEMPLATES = {}

    @classmethod
    def setUpClass(cls):
        setup_test_template_loader(cls.TEMPLATES)

    @classmethod
    def tearDownClass(cls):
        restore_template_loaders()


class TestLoadWidgets(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'dummy.html': '',
        'load_widgets': '''{% load sniplates %}{% load_widgets foo='dummy.html' %}''',
    }

    def test_load_widgets(self):
        ctx = Context()
        tmpl = get_template('load_widgets')
        tmpl.render(ctx)

        self.assertIn(WIDGET_CONTEXT_KEY, ctx.render_context)
