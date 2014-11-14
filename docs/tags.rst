====
Tags
====

There are only a few tags in snipates: load_widgets, widget, form_field and
nested_widget.  There is also a single filter: flatattrs.


The `load_widgets` tag
======================

.. code-block:: django

   {% load_widgets alias=template_name ... %}

This tag is used to load widget libraries from templates.  You can load more
than one library, either at a time, or in separate tags.  Because the widgets
are stored in the render context, not the context, they are available in child
templates even when defined in an inherited template.


The `widget` tag
================

.. code-block:: django

   {% widget 'alias:block_name' .... %}

Renders the specified widget with the current context.  You can provide extra
values to override, just like with `{% include %}`.  Currently does not support
the `only` argument.

The name is composed of the alias specified in the `load_widgets` tag, and the
name of the block in that template, joined with a ':'.


The `form_field` tag
====================

.. code-block:: django

    {% form_field form.fieldname [widget=] [alias=] .... %}

.. note::

   This tag is compatible with the `field` tag from ``formulation``, and can
   use the same templates.

Works like the ``widget`` tag, but "explodes" useful attributes of the field
into the context.

Any extra keyword arguments you pass to the field tag will overwrite values of
the same name.

If `widget` is not specified, it will be determined from the first found of any
block matching the following patterns:

- {field}_{widget}_{name}
- {field}_{name}
- {widget}_{name}
- {field}_{widget}
- {name}
- {widget}
- {field}

These will be looked up within the alias block set "form", unless the alias
keyword is passed to override it.

Values from ``BoundField``
--------------------------

The following values are take from the ``BoundField``:

- css_classes
- errors
- field
- form
- help_text
- html_name
- id_for_label
- label
- name
- value

Values from ``Field``
---------------------

And these from the ``Field`` itself:

- choices
- widget
- required


The `nested_widget` tag
=======================

.. code-block:: django

   {% nested_widget widgetname .... %}
       ...
   {% endnested %}

This tag is a container block that will render its contents, and pass the
output to its widget as 'content'.

An example use of this is for wrapping fields in a fieldset template:

.. code-block:: django

    {% nested_widget 'form:fieldset' caption="About You" %}
        {% form_field form.first_name %} <br>
        {% form_field form.last_name %}
    {% endnested %}


The `flatattrs` filter
=======================

.. code-block:: django

   {{ attrdict|flatarrs }}

This is simply a wrapper around :func:`django.forms.utils.flatatt`

It converts a dict of attributes into a string, in proper key="value" syntax.
The values will be escaped, but keys will not.
