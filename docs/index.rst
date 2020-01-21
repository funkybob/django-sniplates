.. Django Sniplates documentation master file, created by
   sphinx-quickstart on Sat Sep  6 10:23:25 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Sniplates
================

.. rubric:: Efficient template macros

.. image:: https://travis-ci.org/funkybob/django-sniplates.png
              :target: https://travis-ci.org/funkybob/django-sniplates

.. .. image:: https://pypip.in/d/django-sniplates/badge.png
..              :target: https://crate.io/packages/django-sniplates

.. image:: https://img.shields.io/pypi/v/django-sniplates.svg
  :target: https://pypi.python.org/pypi/django-sniplates


Contents:

.. toctree::
   :maxdepth: 2

   tags
   filters
   extractor
   changelog
   formulation

Overview
--------

Have you ever found yourself repeating chunks of your templates, and wishing
Django had a "macro" in templates?

Tried using {% include %} only to find it slow and clumsy?

Introducing Sniplates - the efficient way to provide your template authors with
an arsenal of template macros.

Requirements
------------

Requires Django 2.2 or newer, and is tested against Python  3.5, 3.6, 3.7, 3.8,
PyP and PyPy3.5

Quick-start
-----------

First, install sniplates:

.. code-block:: sh

   pip install django-sniplates

And add it to ``INSTALLED_APPS``.

Next, write a template with your widgets.  Let's go with bootstrap tools, and
call it `widgets/bootstrap.html`

.. code-block:: django

   {% block label %}<span class="label label-{{ label_type|default:'default' }}">{{ text }}</span>{% endblock %}
   {% block alert %}<div class="alert alert-{{ alert_type|default:'success' }}" role="alert">{{ text }}</div>{% endblock %}

Now, in your main template, you need to load the sniplates library.

.. code-block:: django

   {% load sniplates %}

Then load your widget library, and give it an alias:

.. code-block:: django

   {% load_widgets bootstrap="widgets/bootstrap.html" %}

Now, when you need to add a label or alert in your page:

.. code-block:: django

   {% widget "bootstrap:label" text="Things go here" %}
   {% widget "bootstrap:alert" text="It's alive" alert_type="info" %}


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Thanks
======

This project was originally inspired by a feature request by Stephan Sokolow.
