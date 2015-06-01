
from contextlib import contextmanager

try:
    from django.forms.utils import flatatt
except ImportError:  # django 1.4
    from django.forms.util import flatatt
from django import template
from django.template.base import token_kwargs
from django.template.loader import get_template
from django.template.loader_tags import (
    BlockNode, ExtendsNode, BlockContext, BLOCK_CONTEXT_KEY,
)
from django.utils import six
from django.utils.encoding import force_text

register = template.Library()

'''
Sniplates

Re-usable template widgets.

{% load_widgets alias="template.name" .... %}


{% widget 'alias:blockname' .... %}

'''

WIDGET_CONTEXT_KEY = '_widgets_'


def resolve_blocks(template, context):
    '''
    Return a BlockContext instance of all the {% block %} tags in the template.

    If template is a string, it will be resolved through get_template
    '''
    try:
        blocks = context.render_context[BLOCK_CONTEXT_KEY]
    except KeyError:
        blocks = context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()

    # If it's just the name, resolve into template
    if isinstance(template, six.string_types):
        template = get_template(template)

    # For Django 1.8 compatibility
    template = getattr(template, 'template', template)

    # Add this templates blocks as the first
    local_blocks = dict(
        (block.name, block)
        for block in template.nodelist.get_nodes_by_type(BlockNode)
    )
    blocks.add_blocks(local_blocks)

    # Do we extend a parent template?
    extends = template.nodelist.get_nodes_by_type(ExtendsNode)
    if extends:
        # Can only have one extends in a template
        extends_node = extends[0]

        # Get the parent, and recurse
        parent_template = extends_node.get_parent(context)
        resolve_blocks(parent_template, context)

    return blocks


def parse_widget_name(widget):
    '''
    Parse a alias:block_name string into separate parts.
    '''
    try:
        alias, block_name = widget.split(':', 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            'widget name must be "alias:block_name" - %s' % widget
        )

    return alias, block_name


@contextmanager
def using(context, alias):
    '''
    Temporarily update the context to use the BlockContext for the given alias.
    '''

    # An empty alias means look in the current widget set.
    if alias == '':
        yield context
    else:
        try:
            widgets = context.render_context[WIDGET_CONTEXT_KEY]
        except KeyError:
            raise template.TemplateSyntaxError('No widget libraries loaded!')

        try:
            block_set = widgets[alias]
        except KeyError:
            raise template.TemplateSyntaxError(
                'No widget library loaded for alias: %r' % alias
            )

        context.render_context.push()
        context.render_context[BLOCK_CONTEXT_KEY] = block_set
        context.render_context[WIDGET_CONTEXT_KEY] = widgets

        yield context

        context.render_context.pop()


def find_block(context, *names):
    '''
    Find the first matching block in the current block_context
    '''
    block_set = context.render_context[BLOCK_CONTEXT_KEY]
    for name in names:
        block = block_set.get_block(name)
        if block is not None:
            return block

    raise template.TemplateSyntaxError(
        'No widget found for: %r' % (names,)
    )


@register.simple_tag(takes_context=True)
def load_widgets(context, **kwargs):
    '''
    Load a series of widget libraries.
    '''
    _soft = kwargs.pop('_soft', False)

    try:
        widgets = context.render_context[WIDGET_CONTEXT_KEY]
    except KeyError:
        widgets = context.render_context[WIDGET_CONTEXT_KEY] = {}

    for alias, template_name in kwargs.items():
        if _soft and alias in widgets:
            continue

        context.render_context.push()
        context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()

        try:
            blocks = resolve_blocks(template_name, context)
            widgets[alias] = blocks
        finally:
            context.render_context.pop()

    return ''


def pop_asvar(bits):
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        del bits[-2:]
        return asvar


class Widget(template.Node):
    def __init__(self, widget, kwargs, asvar):
        self.widget = widget
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        widget = self.widget.resolve(context)

        alias, block_name = parse_widget_name(widget)

        with using(context, alias):
            block = find_block(context, block_name)

            kwargs = {
                key: val.resolve(context)
                for key, val in self.kwargs.items()
            }
            context.update(kwargs)
            try:
                result = block.render(context)
            finally:
                context.pop()

            if self.asvar:
                context[self.asvar] = result
                return ''

            return result


@register.tag
def widget(parser, token):
    bits = token.split_contents()
    tag_name = bits.pop(0)

    try:
        widget = parser.compile_filter(bits.pop(0))
    except IndexError:
        raise template.TemplateSyntaxError(
            '%s requires one positional argument' % tag_name
        )

    asvar = pop_asvar(bits)

    kwargs = token_kwargs(bits, parser)
    if bits:
        raise template.TemplateSyntaxError(
            '%s accepts only one positional argument' % tag_name
        )

    return Widget(widget, kwargs, asvar)


class NestedWidget(template.Node):
    def __init__(self, widget, nodelist, kwargs, asvar):
        self.widget = widget
        self.nodelist = nodelist
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        widget = self.widget.resolve(context)

        alias, block_name = parse_widget_name(widget)

        with using(context, alias):
            block = find_block(context, block_name)

            kwargs = {
                key: val.resolve(context)
                for key, val in self.kwargs.items()
            }
            context.update(kwargs)
            try:
                content = self.nodelist.render(context)
                try:
                    context.update({'content': content})
                    result = block.render(context)
                finally:
                    context.pop()
            finally:
                context.pop()

            if self.asvar:
                context[self.asvar] = result
                return ''

            return result


@register.tag
def nested_widget(parser, token):
    bits = token.split_contents()
    tag_name = bits.pop(0)

    try:
        widget = parser.compile_filter(bits.pop(0))
    except IndexError:
        raise template.TemplateSyntaxError(
            '%s requires one positional argument' % tag_name
        )

    asvar = pop_asvar(bits)

    kwargs = token_kwargs(bits, parser)

    if bits:
        raise template.TemplateSyntaxError(
            '%s accepts only one positional argument' % tag_name
        )

    nodelist = parser.parse(('endnested',))
    parser.delete_first_token()

    return NestedWidget(widget, nodelist, kwargs, asvar)


@register.simple_tag(takes_context=True)
def form_field(context, field, widget=None, **kwargs):
    if widget is None:
        alias = kwargs.pop('alias', 'form')

        block_names = auto_widget(field)
    else:
        alias, block_name = parse_widget_name(widget)

        block_names = [block_name]

    field_data = {
        'form_field': field,
        'id': field.auto_id,
        'widget_type': field.field.widget.__class__.__name__,
        'field_type': field.field.__class__.__name__,
    }

    for attr in ('css_classes', 'errors', 'field', 'form', 'help_text',
                 'html_name', 'id_for_label', 'label', 'name',):
        field_data[attr] = getattr(field, attr)

    for attr in ('choices', 'widget', 'required'):
        field_data[attr] = getattr(field.field, attr, None)

    # Normalize the value [django.forms.widgets.Select.render_options]
    value = field.value()
    if value is None:
        pass
    elif isinstance(value, (list, tuple)):
        value = map(force_text, value)
    else:
        value = force_text(value)
    field_data['value'] = value

    if field_data['choices']:
        field_data['display'] = dict(field.field.choices).get(field_data['value'], '')
        field_data['choices'] = [
            (force_text(k), v)
            for k, v in field_data['choices']
        ]

    # Allow supplied values to override field data
    field_data.update(kwargs)

    with using(context, alias):
        block = find_block(context, *block_names)

        context.update(field_data)
        try:
            return block.render(context)
        finally:
            context.pop()


def auto_widget(field):
    '''Return a list of widget names for the provided field.'''
    # Auto-detect
    info = {
        'widget': field.field.widget.__class__.__name__,
        'field': field.field.__class__.__name__,
        'name': field.name,
    }

    return [
        fmt.format(**info)
        for fmt in (
            '{field}_{widget}_{name}',
            '{field}_{name}',
            '{widget}_{name}',
            '{field}_{widget}',
            '{name}',
            '{widget}',
            '{field}',
        )
    ]


@register.simple_tag
def show_form(form, alias='forms', normal_row='normal_row', error_row='error_row', help_text='help_text', errors_on_separate_row=True):
    normal_row = lookup_block(alias, normal_row)
    error_row = lookup_block(alias, error_row)
    help_text = lookup_block(alias, help_text)

    # Errors from non-field and hidden fields.
    top_errors = form.non_field_errors()

    for name, field in form.fields.items():
        bf = form[name]

        if bf.is_hidden:
            pass
        else:
            pass
    return ''


@register.filter
def flatattrs(attrs):
    return flatatt(attrs)


@register.simple_tag(takes_context=True)
def reuse(context, block_list, **kwargs):
    '''
    Allow reuse of a block within a template.

    {% reuse '_myblock' foo=bar %}

    If passed a list of block names, will use the first that matches:

    {% reuse list_of_block_names .... %}
    '''
    try:
        block_context = context.render_context[BLOCK_CONTEXT_KEY]
    except KeyError:
        block_context = BlockContext()

    if not isinstance(block_list, (list, tuple)):
        block_list = [block_list]

    for block in block_list:
        block = block_context.get_block(block)
        if block:
            break
    else:
        return ''

    context.update(kwargs)
    try:
        return block.render(context)
    finally:
        context.pop()
