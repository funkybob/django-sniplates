
from django.template import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .utils import TemplateTestMixin


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


class TestInheritance(TemplateTestMixin, SimpleTestCase):
    TEMPLATES = {
        'base': '''DOCUMENT {% block content %}{% endblock %}''',
        'block_overlap_widgets': '''{% block foo %}foo{% endblock %}''',
        'block_overlap': '''{% extends 'base' %}{% load sniplates %}{% load_widgets foo='block_overlap_widgets' %}{% block content %}content {% widget 'foo:bar' %}{% endblock %}{% block bar %}bar{% endblock %}''',

        'parent_inherit': '''{% extends 'parent_inherit_base' %}{% load sniplates %}{% block content %}{% widget 'foo:test' %}{% endblock %}''',
        'parent_inherit_base': '''{% load sniplates %}{% load_widgets foo='parent_inherit_widgets' %}{% block content %}{% endblock %}''',
        'parent_inherit_widgets': '''{% block test %}foo{% endblock %}''',

        'parent_overlap': '''{% load sniplates %}{% load_widgets foo='parent_overlap_widgets' %}{% block main %}first{% endblock%}''',
        'parent_overlap_widgets': '''{% block main %}second{% endblock %}''',
     }

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

        self.assertEqual(output, 'foo')

    def test_parent_overlap(self):
        '''
        If a sniplate library has a block of the same name as in the calling
        template, we should NOT override it.
        '''
        tmpl = get_template('parent_overlap')
        output = tmpl.render(self.ctx)

        self.assertEqual(output, 'first')
