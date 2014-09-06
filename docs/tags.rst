Tags
====

There are only two tags in snipates: load_widgets and widget


The `load_widgets` tag
----------------------

.. code-block:: django

   {% load_widgets alias=template_name ... %}

This tag is used to load widget libraries from templates.  You can load more
than one library, either at a time, or in separate tags.  Because the widgets
are stored in the render context, not the context, they are available in child
templates even when defined in an inherited template.


The `widget` tag
----------------

.. code-block:: django

   {% widget 'alias:block_name' .... %}

Renders the specified widget with the current context.  You can provide extra
values to override, just like with `{% include %}`.  Currently does not support
the `only` argument.

The name is composed of the alias specified in the `load_widgets` tag, and the
name of the block in that template, joined with a ':'.

