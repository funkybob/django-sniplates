import datetime
from contextlib import contextmanager

from django import template
from django.forms.utils import flatatt
from django.forms.widgets import DateTimeBaseInput
from django.template.base import token_kwargs
from django.template.loader import get_template
from django.template.loader_tags import BLOCK_CONTEXT_KEY, BlockContext, BlockNode, ExtendsNode
from django.utils.encoding import force_str
from django.utils.functional import cached_property

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
    if isinstance(template, str):
        template = get_template(template)

    # For Django 1.8 compatibility
    template = getattr(template, 'template', template)

    # Add this templates blocks as the first
    local_blocks = {
        block.name: block
        for block in template.nodelist.get_nodes_by_type(BlockNode)
    }
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
        raise template.TemplateSyntaxError('widget name must be "alias:block_name" - %s' % widget)

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
            raise template.TemplateSyntaxError('No widget library loaded for alias: %r' % alias)

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

    raise template.TemplateSyntaxError('No widget found for: %r' % (names,))


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

        with context.render_context.push({BLOCK_CONTEXT_KEY: BlockContext()}):
            blocks = resolve_blocks(template_name, context)
            widgets[alias] = blocks

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
            with context.push(kwargs):
                result = block.render(context)

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
        raise template.TemplateSyntaxError('%s requires one positional argument' % tag_name)

    asvar = pop_asvar(bits)

    kwargs = token_kwargs(bits, parser)
    if bits:
        raise template.TemplateSyntaxError('%s accepts only one positional argument' % tag_name)

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

            with context.push(kwargs):
                content = self.nodelist.render(context)
                with context.push({'content': content}):
                    result = block.render(context)

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
        raise template.TemplateSyntaxError('%s requires one positional argument' % tag_name)

    asvar = pop_asvar(bits)

    kwargs = token_kwargs(bits, parser)

    if bits:
        raise template.TemplateSyntaxError('%s accepts only one positional argument' % tag_name)

    nodelist = parser.parse(('endnested',))
    parser.delete_first_token()

    return NestedWidget(widget, nodelist, kwargs, asvar)


class ChoiceWrapper(tuple):

    def __new__(cls, value=None, display=None):
        tuple_args = [value, display]
        return super(ChoiceWrapper, cls).__new__(cls, tuple(tuple_args))

    def __init__(self, value, display):
        self.value = force_str(value)
        self._display = display

    def __repr__(self):
        return 'ChoiceWrapper(value=%s, display=%s)' % (self.value, self.display)

    def __iter__(self):
        # overriden from tuple to retrun the formatted display
        yield self.value
        yield self.display

    def is_group(self):
        return isinstance(self._display, (list, tuple))

    @property
    def display(self):
        """
        When dealing with optgroups, ensure that the value is properly force_str'd.
        """
        if not self.is_group():
            return self._display
        return ((force_str(k), v) for k, v in self._display)


class FieldExtractor(dict):
    '''
    Base class for extracting Field details.
    Acts as a dict so we can push it on the context stack.
    '''
    def __init__(self, field):
        self.form_field = field
        self.update({
            'id': field.auto_id,
            'widget_type': field.field.widget.__class__.__name__,
            'field_type': field.field.__class__.__name__,
        })

        for attr in (
            'css_classes', 'errors', 'field', 'form', 'help_text', 'html_name', 'id_for_label', 'label', 'name',
        ):
            self[attr] = getattr(field, attr)

        for attr in ('widget', 'required', 'disabled'):
            self[attr] = getattr(field.field, attr, None)

    def __contains__(self, key):
        '''
        Context uses 'if key in ...'
        '''
        return key in self.keys() or hasattr(self, key)

    def __missing__(self, key):
        return getattr(self, key)

    @cached_property
    def raw_value(self):
        return self.form_field.value()

    @cached_property
    def value(self):
        if isinstance(self.raw_value, (tuple, list)):
            return [force_str(bit) for bit in self.raw_value]
        return force_str(self.raw_value)

    @cached_property
    def initial(self):
        data = self.form_field.form.initial.get(self.form_field.name, self.form_field.field.initial)
        if callable(data):
            data = data()
            # If this is an auto-generated default date, nix the
            # microseconds for standardized handling. See #22502.
            if (
                isinstance(data, (datetime.datetime, datetime.time)) and
                not self.field.widget.supports_microseconds
            ):
                data = data.replace(microsecond=0)
        return self.form_field.field.prepare_value(data)

    @cached_property
    def display(self):
        '''Display value for selected choice.'''
        return dict(self.choices).get(self.value, '')

    @cached_property
    def choices(self):
        c = self.form_field.field.choices
        if not c:
            return c
        return tuple(
            ChoiceWrapper(value=k, display=v)
            for k, v in self.form_field.field.choices
        )


class FileFieldExtractor(FieldExtractor):

    @cached_property
    def file_size(self):
        if self.raw_value:
            return self.raw_value.size

    @cached_property
    def url(self):
        if self.raw_value:
            return self.raw_value.url


class ImageFieldExtractor(FileFieldExtractor):

    @cached_property
    def width(self):
        if self.value:
            return self.value.width

    @cached_property
    def height(self):
        if self.value:
            return self.value.height


class NullBooleanFieldExtractor(FieldExtractor):

    @cached_property
    def raw_value(self):
        """
        When the value is None, it's actually rendered as 'unknown', see
        ``django.forms.widgets.NullBooleanSelect.__init__``
        """
        raw_value = super().raw_value
        if raw_value is None:
            return 'unknown'
        return raw_value

    @cached_property
    def value(self):
        """
        Maps True/False and 2/3 to the correct stringified version.

        See ``django.forms.widgets.NullBooleanSelect.value_from_datadict``.
        """
        try:
            return {
                True: 'true',
                False: 'false',
                'true': 'true',
                'false': 'false',
                'True': 'true',
                'False': 'false',
                '2': 'true',
                '3': 'false'
            }[self.raw_value]
        except KeyError:
            return 'unknown'

    @cached_property
    def choices(self):
        c = self['widget'].choices
        if not c:
            return c

        return tuple(
            ChoiceWrapper(value=force_str(k), display=v)
            for k, v in c
        )


class DateTimeBaseExtractor(FieldExtractor):
    """
    Applies the date/time/datetime formatting to the value.
    """

    @cached_property
    def value(self):
        if isinstance(self['widget'], DateTimeBaseInput):
            return self['widget'].format_value(self.raw_value)
        # if it's a different widget, fall back to the default
        return super(DateTimeBaseExtractor, self).value


# Map of field types to functions for extracting their data
EXTRACTOR = {
    'FileField': FileFieldExtractor,
    'ImageField': ImageFieldExtractor,
    'NullBooleanField': NullBooleanFieldExtractor,
    'DateField': DateTimeBaseExtractor,
    'DateTimeField': DateTimeBaseExtractor,
    'TimeField': DateTimeBaseExtractor,
}


@register.simple_tag(takes_context=True)
def form_field(context, field, widget=None, **kwargs):
    if not field:
        raise template.TemplateSyntaxError('form_field requires a value field as first argument')

    if widget is None:
        alias = kwargs.pop('alias', 'form')

        block_names = auto_widget(field)
    else:
        alias, block_name = parse_widget_name(widget)

        block_names = [block_name]

    field_type = field.field.__class__.__name__
    field_data = EXTRACTOR.get(field_type, FieldExtractor)(field)

    # Allow supplied values to override field data
    field_data.update(kwargs)

    with using(context, alias):
        block = find_block(context, *block_names)

        try:
            context.dicts.append(field_data)
            return block.render(context)
        finally:
            context.dicts.pop()


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

    for block_name in block_list:
        block = block_context.get_block(block_name)
        if block:
            break
    else:
        return ''

    with context.push(kwargs):
        return block.render(context)
