=========
Changelog
=========

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
