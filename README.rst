Caktus Jade Truffle Django Project
==================================

Jade Truffle is a `cookiecutter`_ template designed to generate a greenfield Django 3.0
or Wagtail project.

Requirements
~~~~~~~~~~~~
* Python 3.8
* pip-tools
* cookiecutter
* A virtual environment manager

Installation
~~~~~~~~~~~~

Create a Python virtual envionment with your tool of choice. For purposes
of these intructions we'll call the envionment ``jade-truffle``.

Enable your environment and install cookiecutter::

    $(jade-truflle) pip install cookiecutter

Now you have an environment that can install cookiecutter templates.

Next use cookiecutter to build a project using ``jade-truflle``::

    $(jade-truffle) cookiecutter https://github.com/caktus/jade-truffle


Options
~~~~~~~

The cookiecutter will run through a series of configuration options

1. Project Name
    * This can be anything you like (e.g. Apple Pie)
2. Projet Slug:
    * The slug will be generated from the Project Name, but can be overriden.
    * The slug will be used in most configuration options in the generated project.
            * ``apple_pie/apple_pie/settings``
            * ``apple_pie/apple_pie/urls.py``
3. Project Type: ``django`` or ``wagtail``
4. Postgres Port: Defaults to [5432]
    * This is used for local dev so you can set this to any port you like
5. Primary App: Will be used as the main app in the projects apps directory.
    * For example: ``apple_pie/apps/apple_pie``
6. Project Domain Name:
    * Defaults to ``caktus-built.com``





.. _cookiecutter: https://github.com/cookiecutter/cookiecutter