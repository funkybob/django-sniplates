
from django.template import Context, TemplateSyntaxError
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

    def setUp(self):
        self.ctx = Context()


class TestLoadWidgets(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'simple.html': '''{% block simple %}success{% endblock %}''',
        'other.html': '''{% block other %}winning{% endblock %}''',
        'load_widgets': '''{% load sniplates %}{% load_widgets foo='simple.html' %}{% widget "foo:simple" %}''',
        'load_widgets_two': '''{% load sniplates %}{% load_widgets foo='simple.html' bar='other.html' %}{% widget 'foo:simple' %}<=>{% widget 'bar:other' %}''',
        'load_widgets_three': '''{% load sniplates %}{% load_widgets foo='simple.html' %}{% load_widgets bar='other.html' %}{% widget 'foo:simple' %}<=>{% widget 'bar:other' %}''',
    }

    def test_load_widgets(self):
        tmpl = get_template('load_widgets')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'success')

    def test_load_widgets_two(self):
        tmpl = get_template('load_widgets_two')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'success<=>winning')

    def test_load_widgets_three(self):
        tmpl = get_template('load_widgets_three')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'success<=>winning')


class TestInvalid(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'simple.html': '''{% block simple %}success{% endblock %}''',
        'bad_name': ''' {% load sniplates %}{% widget 'boo-bar' %}''',
        'not_loaded': '''{% load sniplates %}{% widget 'foo:bar' %}''',
        'no_lib': '''{% load sniplates %}{% load_widgets foo='simple.html' %}{% widget 'bar:no_lib' %}''',
        'no_widget': '''{% load sniplates %}{% load_widgets foo='simple.html' %}{% widget "foo:no_widget" %}''',
    }

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


class TestWidgetTag(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'widgets.one': '''
{% block fixed %}fixed{% endblock %}
{% block var %}{{ var }}{% endblock %}
{% block default %}{{ var|default:'default' }}{% endblock %}
        ''',
        'widgets.two': '''
{% extends 'widgets.one' %}
{% block var %}more {{ var }}{% endblock %}
        ''',

        'fixed': '''{% load sniplates %}{% load_widgets foo='widgets.one' %}{% widget 'foo:fixed' %}''',
        'var': '''{% load sniplates %}{% load_widgets foo='widgets.one' %}{% widget 'foo:var' var='value' %}''',
        'inherit': '''{% load sniplates %}{% load_widgets foo='widgets.two' %}{% widget 'foo:var' var='value' %}''',
    }

    def test_fixed(self):
        tmpl = get_template('fixed')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'fixed')

    def test_var(self):
        tmpl = get_template('var')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'value')

    def test_inherit(self):
        tmpl = get_template('inherit')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'more value')
