Caktus Jade Truffle Django Project
==================================

Jade Truffle is the Mandarin traslation of the cacti species *blossfeldia liliputana*. The smallest of all cacti. 

Jade Truffle is a `cookiecutter`_ template designed to generate a greenfield Django 3.0
or Wagtail project.

Jad Truffle is a work in progress. The intention is to make the base project quickly deployable, while
at the same time allowing for project specific overrides.  

Currently the template is highly tuned to an AWS/EKS deployment methodology using `Django K8s`_, `AWS Web Stacks`_,
and `K8s Web Cluster`_. The hope is that future work will add to the deployment methods.

Requirements
~~~~~~~~~~~~
* Python 3.8
* pip-tools
* cookiecutter
* A virtual environment manager
* direnv

Installation
~~~~~~~~~~~~

Create a Python virtual environment with your tool of choice. For purposes
of these intructions we'll call the environment ``jade-truffle``.

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
    * Generated from the Project Name, but can be overriden.
    * Used in most configuration options in the generated project.
            * ``apple_pie/apple_pie/settings``
            * ``apple_pie/apple_pie/urls.py``
3. Project Type: ``django`` or ``wagtail``

4. Testing Type: ``django`` or ``pytest``

5. CSS Style: ``sass`` or ``roll-my-own``

6. Postgres Port: Defaults to [5432]
    * This is used for local dev so you can set this to any port you like
7. Primary App: Will be used as the main app in the projects apps directory.
    * For example: ``apple_pie/apps/apple_pie``
8. Project Domain Name:
    * Defaults to ``caktus-built.com``

The generated project has a README that details the steps for install.

.. TODO: Add more documentation about the structure of this template.


.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _Django K8s: https://github.com/caktus/ansible-role-django-k8s
.. _AWS Web Stacks: https://github.com/caktus/ansible-role-aws-web-stacks
.. _K8s Web Cluster: https://github.com/caktus/ansible-role-k8s-web-cluster