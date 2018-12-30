=========
Changelog
=========

0.6.0 (2018-08-08)
------------------

.. note: Support for Django < 2.0 has been officially dropped.

Features:

- Now also extracts `disabled` from form fields.

Bugs fixed:

- Password fields no longer render their value
- Labels now have the correct ID value in their for attribute.
- Date inputs format correctly.

0.5.0 (2016-08-16)
------------------

Features:

- Add coverage to runtests.py
- Added `initial` property to FieldExtractor
- Added Extractors for date, datetime and time fields [Sergei Maertens]
- Added Django 1.10 support

Bugs Fixed:

- Rewrote ChoiceWrapper [kezabelle with help from Sergei Maertens]
- Raise TemplateSyntaxError when falsey value passed to {% form_field %}
  [kezzabelle]

Backwards incompatible changes:

- Dropped Django 1.7 support

0.4.1 (2016-01-25)
------------------

Features:

- Fixed default django.html template to use raw_value [Sergei Maertens]
- Added NullBooleanFieldExtractor

Bugs Fixed;

- Made choices lazy again - regression in 0.4 merge [Sergei Maertens]

Testing:

- Switched to having travis use tox [Sergei Maertens]

0.4.0 (2016-01-24)
------------------

.. note:: This app is no longer compatible with Django versions older than 1.6

.. note:: The values in the `file` dict previously added by `form_field` are
          now exploded directly into the context.

Features:

- Added pluggable FieldExploder classes
- Added ``raw_value`` to Form Field exploded attributes
- ``choices`` and ``display`` are now lazy

Bugs Fixed:

Backwards incompatible:

- Your form widgets may need updates related to ``value`` and ``raw_value``.
  ``value`` is no longer cleaned for a proper string-version. Consult
  ``sniplates/django.html`` for a guideline.

0.3.2
-----

Features:

- Explode details from FileField [Thanks mattmcc]

Bugs Fixed:

- Fixed use of 'flatattrs' in templates
- Added ClearableFileInput to default template [Thanks mattmcc]
- Corrected packaging to include templates [Thanks kezabelle]

0.3.1
-----

Bugs Fixed:

- Only set 'display' when value is a scalar.
- BoundField.value is a callable
- Always normalise value, not just when we have choices
- Mark flatatt safe for Django 1.4

0.3.0
-----

Features:

- Reworked to no longer copy() the context - ever!
- Now sets the right block context when rendering widgets so {{ block.super }} works.  Thanks Schinckel!
- Added default Django widget template.
- Added Django 1.8 compatibility.
- Added ``_soft`` option to {% load_widgets %} to avoid reloading an alias.
- Added "as foo" support to {% widget %} and {% nested_widget %}.  Thanks Schinckel!
- A blank alias to {% widget %} and {% nested_widget %} will use the current template context.
- {% reuse %} will now accept a list of block names to search for.

Bugs Fixed:

- Don't lose widget context when inside a widget.  Thanks Schinckel!

Testing:

- Test on pypy3
- Removed testing for Django 1.5 and 1.6.
- Fixed test discovery on Django 1.4.  Thanks Schinckel!

0.2.2
-----

Bugs fixed:

- Fix forcing multi-value fields to unicode in form tag

0.2.1
-----

Features:

- Added `reuse` tag.
- Added 'widget_type' and 'field_type' to exploded data in form_field
- Added 'display' to exploded data in form_field

0.2.0
-----

.. note::  This release now encompases equivalent functionality to
   ``formulation``.

Features:

- Added `nested_widget` tag to allow widgets to contain template content.
- Added `form_field` tag to ease rendering form fields
- Added `flatarr` filter to help with rendering form fields.

Bugs fixed:

- Fix overlap problem when loading more than one widget lib in a single
  `load_widgets` tag.

0.1.1
-----

Bugs fixed:

- Fix overlap problem where a widget libs blocks would override those of the
  loading template.

0.1.0
-----

Initial release
