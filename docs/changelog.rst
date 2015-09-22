=========
Changelog
=========

0.4.0 (2015-09-??)
------------------

.. note:: This app is no longer compatible with Django versions older than 1.6

.. note:: The values in the `file` dict previously added by `form_field` are
          now exploded directly into the context.

Features:

- Added pluggable FieldExploder classes
- Added `raw_value` to Form Field exploded attributes
- `choices` and `display` are now lazy

Bugs Fixed:

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
