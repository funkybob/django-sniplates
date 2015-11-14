=======
Filters
=======

The `flatattrs` filter
=======================

.. code-block:: django

   {{ attrdict|flatarrs }}

This is simply a wrapper around :func:`django.forms.utils.flatatt`

It converts a dict of attributes into a string, in proper key="value" syntax.
The values will be escaped, but keys will not.


The `visible_fields` and `hidden_fields` filters
================================================

.. code-block:: django

   {% for field in form|hidden_fields %}
       {% form_field field %}
   {% endfor %}

These filters yield a list of visible and hidden fields, respectively, from the
form.
