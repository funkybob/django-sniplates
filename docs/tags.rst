====
Tags
====

The sniplates app consists solely of a custom template tag library.

The `load_widgets` tag
======================

.. code-block:: django

   {% load_widgets alias=template_name ... %}

This tag is used to load widget libraries from templates.  You can load more
than one library, either at a time, or in separate tags.  Because the widgets
are stored in the render context, not the context, they are available in child
templates even when defined in an inherited template.

If you pass `_soft=True` any alias that already exists will be skipped.  This
can be helpful to allow templates to ensure they have the widget sets they need
without causing duplicate loads.

.. caution::

   Because of how Django's templates work, if you are using this in a template
   which inherits from another, it MUST be inside a {% block %} tag.

   Any content in a template starting with {% extends %} which it outside a
   {% block %} tag is ignored and never rendered.

The `widget` tag
================

.. code-block:: django

   {% widget 'alias:block_name' ...  [as asvar] %}

Renders the specified widget with the current context.  You can provide extra
values to override, just like with `{% include %}`.  Currently does not support
the `only` argument.

The name is composed of the alias specified in the `load_widgets` tag, and the
name of the block in that template, joined with a ':'. If you use an "empty"
alias, the block will be searched for in the current template (and any
templates it extends).  This form can be used without a `load_widgets` tag.

You may use the `as` form of the tag to store the result of the block in the
context variable you supply instead of rendering it in the template.


The `form_field` tag
====================

.. code-block:: django

    {% form_field form.fieldname [widget=] [alias=form] .... %}

Works like the ``widget`` tag, but extracts useful attributes of the field into
the context.

The values are extracted using a `FieldExtractor <extractor>`_ class, selected according to the form field class.

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

.. note::
    These will be looked up within the alias block set "**form**", unless the
    ``alias`` keyword is passed to override it.

By way of example, given the following form::

    from django.forms import Form, CharField, TextInput

    class MyForm(Form):
        example_field = CharField(widget=TextInput)

using ``{% form_field myform.example_field %}`` without `widget` would look
for a block with one of the following names, in the following order:

- ``CharField_TextInput_example_field``
- ``CharField_example_field``
- ``TextInput_example_field``
- ``CharField_TextInput``
- ``example_field``
- ``TextInput``
- ``CharField``


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

If the field is a FileField, an extra value `file` will be added, which
contains the size and url attributes of the current file.  If it's an
ImageField, the width and height may also be avaialble.

Values from ``Field``
---------------------

And these from the ``Field`` itself:

- choices
- widget
- required

If the field is a ChoicesField, an extra value `display` will be added, which
is the display value for the current value, if any.

The `nested_widget` tag
=======================

.. code-block:: django

   {% nested_widget widgetname .... [as asvar] %}
       ...
   {% endnested %}

This tag is a container block that will render its contents, and pass the
output to its widget as 'content'.

An example use of this is for wrapping fields in a fieldset template:

.. code-block:: django

   {% block fieldset %}
       <fieldset>
       {% if caption %}<caption>{{ caption }}</caption>{% endif %}
       {{ content }}
   {% endblock %}

And would be used as follows:

.. code-block:: django

    {% nested_widget 'form:fieldset' caption="About You" %}
        {% form_field form.first_name %} <br>
        {% form_field form.last_name %}
    {% endnested %}

This tag also supports storing the result in a context variable of your choice
instead of rendering immediately.


The `reuse` tag
===============

.. code-block:: django

   {% reuse blockname ... %}

Much like the `widget` tag, this re-renders an existing block tag in situ.
However, instead of looking for the block in a loaded widget library, it
searches the current template.  This allows templates extending a base to
define reusable "macro" blocks, without having to load a separate widget set.

As with other tags, you can extend the context by passing keyword arguments.

.. note:: This tag only works in templates that {% extends %} another template.
