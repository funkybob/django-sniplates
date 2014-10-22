
from copy import copy

from django import template
from django.template.loader import get_template
from django.template.loader_tags import (
    BlockNode, ExtendsNode, BlockContext, BLOCK_CONTEXT_KEY,
)
from django.utils import six

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

    If template is a string, it will be resovled through get_template
    '''
    try:
        blocks = context.render_context[BLOCK_CONTEXT_KEY]
    except KeyError:
        blocks = context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()

    # If it's just the name, resolve into template
    if isinstance(template, six.string_types):
        template = get_template(template)

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


@register.simple_tag(takes_context=True)
def load_widgets(context, **kwargs):
    '''
    Load a series of widget libraries.
    '''

    try:
        widgets = context.render_context[WIDGET_CONTEXT_KEY]
    except KeyError:
        widgets = context.render_context[WIDGET_CONTEXT_KEY] = {}

    safe_context = copy(context)
    safe_context.render_context = safe_context.render_context.new({
        BLOCK_CONTEXT_KEY: BlockContext(),
    })

    # XXX Should we deal with stacking?
    for alias, template_name in kwargs.items():
        blocks = resolve_blocks(template_name, safe_context)
        widgets[alias] = blocks

    return ''


@register.simple_tag(takes_context=True)
def widget(context, widget, **kwargs):
    try:
        alias, block_name = widget.split(':', 1)
    except ValueError:
        raise template.TemplateSyntaxError('widget name must be "alias:block_name" - %s' % widget)

    try:
        widgets = context.render_context[WIDGET_CONTEXT_KEY]
    except KeyError:
        raise template.TemplateSyntaxError("No widget libraries loaded!")

    try:
        block_set = widgets[alias]
    except KeyError:
        raise template.TemplateSyntaxError('No widget library loaded for alias: %r' % alias)

    block = block_set.get_block(block_name)
    if block is None:
        raise template.TemplateSyntaxError('No widget named %r in set %r' % (block_name, alias))

    context.update(kwargs)
    try:
        return block.render(context)
    finally:
        context.pop()
