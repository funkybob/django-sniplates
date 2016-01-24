==============
FieldExtractor
==============

The ``FieldExtractor`` class defines which properties are extracted from Form
Fields and made available in the rendering context.

Extractors are registered in the sniplates.EXTRACTOR dict, mapping the Field
class name to the exploder class to use.

The default ``FieldExtractor`` copies the following attributes from the
``BoundField``:

- css_classes
- errors
- field
- form
- help_text
- html_name
- id_for_label
- label
- name

It also copies the following attributse from the ``Field``:

- widget
- required

In addition, it will lazily evaluate the following:

raw_value
    The raw value of the field.

value
    The raw value forced to text.

display
    The matching display value from the choices list for the current value, if
    this field has a value and a choices list.  Otherwise empty string.

choices
    A tuple of ``ChoiceWrapper`` instances. ``ChoiceWrapper`` is a named tuple
    with the attributes ``value`` and ``display``. It has one extra method:
    ``is_group`` which returns ``True`` for option-groups.
    ``ChoiceWrapper.value`` is forced to text.


Sub-classes provided
====================

Three ``FieldExtractor`` sub-classes are provided out of the box:

``FileFieldExtractor`` adds ``file_size`` and ``url`` to the context.

``ImageFieldExtractor`` extends ``FileFieldExtractor``, and adds ``length`` and
``width`` also.

``NullBooleanFieldExtractor`` makes ``NullBooleanField`` compatible with the
default ``Select`` widget.


Providing your own extractors
=============================

It's possible to write your own extractor and add it `to Sniplates`. You can
use Django's ``django.apps.AppConfig`` for this.

Example:

.. code-block:: python

    # file myapp/extractors.py

    from sniplates.templatetags.sniplates import FieldExtractor


    class MultipleModelChoiceExtractor(FieldExtractor):

        @property
        def selected_instances(self):
            queryset = self.form_field.field.queryset
            if len(self.raw_value):
                return queryset.filter(pk__in=self.raw_value)
            return queryset.none()


This would give you access to the queryset of selected instances in
the field widget:

.. code-block:: django

    {% for obj in selected_instances %}
        {{ obj }}
    {% endfor %}

Registering it with Sniplates is done with the ``AppConfig``:

.. code-block:: python

    # myapp/apps.py

    from django.apps import AppConfig


    class KitsConfig(AppConfig):
        name = 'myapp'

        def ready(self):
            # register the custom extractor
            from sniplates.templatetags.sniplates import EXTRACTOR
            from .extractors import MultipleModelChoiceExtractor
            EXTRACTOR['MultipleModelChoiceField'] = MultipleModelChoiceExtractor
