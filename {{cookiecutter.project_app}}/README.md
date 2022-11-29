# {{ cookiecutter.project_name }}


## ✏️ **Develop**
To begin you should have the following applications installed on your local development system:

- Python >= 3.8
- NodeJS == 12.x
- npm == 6.14.x (comes with node 12)
- [nvm](https://github.com/nvm-sh/nvm/blob/master/README.md) is not strictly _required_, but will almost certainly be necessary unless you just happen to have Node.js 12.x installed on your machine.
- [pip](http://www.pip-installer.org/) >= 20
- Postgres >= 12
- git >= 2.26

{% if cookiecutter.css_style == "sass" %}
### 🤷‍♂️ **Making changes to templates or stylesheets?**
This project uses [django-sass-processor](https://pypi.org/project/django-sass-processor/) for sass compilation and stylesheet management.

#### Stick to the following conventions when adding new templates
A template is one of:
1. page
  - these should be named `[page_name]_page.html`, lives in the templates/pages directory
2. include
  - no naming convention, lives in the  templates/includes directory
3. base
  - these are for high-level layout base-templates

#### Stylesheets follow the same convention. Stylesheets for pages live in the static/styles/pages directory, and so on.

#### To include a **new scss file** in a template, do the following:

Name your file according to the following convention:
1. If your scss file is going to be linked to directly from a template, as below, name the file `[template_name].scss`
2. If your scss file is only going to be imported by another scss file using the `@import` directive, prepend the filename with an underscore: `_[my_sass_file].scss` then link to it in your template using the django-sass-processor provided `sass_tags`.

{% raw %}
```html
{% load sass_tags %}
<link href="{% sass_src '[app]/styles/[includes,pages,blocks]/[template-name].scss' %}" rel="stylesheet" type="text/css" />
```
{% endraw %}
We're doing our best to follow BEM, [Here's](https://www.smashingmagazine.com/2018/06/bem-for-beginners/) a little reading on BEM.


When styling, keep the following conventions in mind:
- If you're creating a new template, create a new stylesheet.
- Every stylesheet has its own brief documentation including
1. an "Index" describing the contents per BEM "block".
2. a description of each BEM "block"
- Keep it as flat as possible. Try to only nest state changes, like ":hover" or ".open".
- Is there a variable for that?
- REM is set up to change size based on screen width. Keep this in mind. You might actually want pixels!

{% endif %}

### 💪 **Setup Manually**

**1. Get the project**

First clone the repository from Github and switch to the new directory:

```linux
    $ git clone git@github.com:caktus/{{ cookiecutter.project_app }}.git
    $ cd {{ cookiecutter.project_app }}
```

**2. Set up virtual environment**

Next, set up your virtual environment with python3. For example, ``{{ cookiecutter.project_app }}``.

You will note the distinct lack of opinion on how you should manage your virtual environment. This is by design.


**3. Install dependencies**

``nvm`` is preferred for managing Node versions and ``.nvmrc`` contains the
specific Node version for this project. To install the correct (and latest)
Node version run:

```sh
    ({{ cookiecutter.project_app }})$ nvm install
```

Now install the project Node packages with ``npm``:

```sh
    ({{ cookiecutter.project_app }})$ npm install
```

Install Python dependencies with:

```linux
    ({{ cookiecutter.project_app }})$ make setup
```

{% if cookiecutter.include_accessibility_tests == 'yes' %}
This project has been set up to run automated accessibility tests,
which require [geckodriver](https://github.com/mozilla/geckodriver/).

To install on Linux:

```
$ curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz > geckodriver.tar.gz
$ tar -zxvf geckodriver.tar.gz
$ mv geckodriver /usr/local/bin
```

To install on Mac:

```
$ brew install geckodriver
```
{% endif %}

NOTE: This project uses ``pip-tools``. If the dependency `.txt` files need to be
updated:

```sh
    ({{ cookiecutter.project_app }})$ make update_requirements setup
```

NOTE 2: During a development cycle if a developer needs to add subtract or modify the requirements of the project, the
workflow is to:

1) Make the change in the ``*.in`` requirement file
2) run ``make update_requirements``
3) commit both ``*.in`` file(s) and the ``*.txt`` file(s) generated


**4. Pre-commit**

pre-commit is used to enforce a variety of community standards. CI runs it,
so it's useful to setup the pre-commit hook to catch any issues before pushing
to GitHub and reset your pre-commit cache to make sure that you're starting fresh.

To install, run:

```linux
    ({{ cookiecutter.project_app }})$ pre-commit clean
    ({{ cookiecutter.project_app }})$ pre-commit install
```


**5. Set up local env variables**

Next, we'll set up our local environment variables. We use
[django-dotenv](https://github.com/jpadilla/django-dotenv) to automatically read
environment variables located in a file named `.env` in the top level directory of the
project (but you may use any other way of setting environment variables, like direnv or
manually setting them). The only variable we need to start is `DJANGO_SETTINGS_MODULE`:

```linux
    ({{ cookiecutter.project_app }})$ cp {{ cookiecutter.project_app }}/settings/local.example.py {{ cookiecutter.project_app }}/settings/local.py
    ({{ cookiecutter.project_app }})$ echo "DJANGO_SETTINGS_MODULE={{ cookiecutter.project_app }}.settings.local" > .env
```


**6. Database**

The setup for local development assumes that you will be working with dockerized
services.

First add the following line to your `.env` file:

```sh
({{ cookiecutter.project_app }})$ echo "DATABASE_URL=postgres://postgres@127.0.0.1:{{ cookiecutter.postgres_port }}/{{ cookiecutter.project_app }}" >> .env
```

The `docker-compose.yml` sets up environment variables in a file, ``.postgres``.
To use the Docker setup, add these lines to that file:

```sh
    POSTGRES_DB={{ cookiecutter.project_app }}
    POSTGRES_HOST_AUTH_METHOD=trust
```

If you want to connect to the database from your host machine, export the
following shell environment variables:

```sh
    export PGHOST=127.0.0.1
    export PGPORT={{ cookiecutter.postgres_port }}
    export PGUSER=postgres
    export PGDATABASE={{ cookiecutter.project_app }}
```


**7. Migrate and create a superuser**

```linux
    ({{ cookiecutter.project_app }})$ docker-compose up -d
    ({{ cookiecutter.project_app }})$ python manage.py migrate
    ({{ cookiecutter.project_app }})$ python manage.py createsuperuser
```

**8. Run the server**

```linux
    ({{ cookiecutter.project_app }})$ docker-compose up -d
    ({{ cookiecutter.project_app }})$ make run-dev
```

After initial setup the development server should be run using ``make run-dev`` this will remove any deployment containers hanging around and setup using local sources and database.


**9. Access the server**

The Django admin is at `/admin` and the Wagtail admin is at `/cms`.


**10. Run tests**

{{ cookiecutter.project_app }} uses pytest as a test runner.


```sh
    ({{ cookiecutter.project_app }})$ make run-tests
```

**11. Reset Media and Database**

{{ cookiecutter.project_app }} uses invoke for interactions with the deployed environments.

From time to time it may become necessary to sync your local media tree with either production or staging. In order to do so,
you will need be setup to communicate with the kubernetes cluster. See [Caktus AWS Account Management](https://github.com/caktus/caktus-hosting-services/blob/main/docs/aws-assumerole.md)
for detailed instructions on authentication.

NOTE: That page will also have the ROLE_ARN you need to switch contexts below.

Once you have access you can run the following command:

```shell
    ({{ cookiecutter.project_app }})$ inv aws.configure-eks-kubeconfig
```

If you have done this in the past, you just need to switch to the correct cluster, run:

```shell
    ({{ cookiecutter.project_app }})$ kubectl config use-context <ROLE_ARN>
```

**Media Reset**

The command for resetting your local media (assuming your local media is found at ``.\media``) is:


```sh
    ({{ cookiecutter.project_app }})$ inv staging {{cookiecutter.cloud_provider}}.sync-media --sync-to="local" --bucket-path="media"
```

If you wish to make sure you need to reset you can issue the command with a ``dry-run`` argument.


```sh
    ({{ cookiecutter.project_app }})$ inv staging {{cookiecutter.cloud_provider}}.sync-media --sync-to="local" --bucket-path="media" --dry-run
```

If you wish to clean out your local media tree before reset you can issue the command with a ``--delete`` argument.


```sh
    ({{ cookiecutter.project_app }})$ inv staging {{cookiecutter.cloud_provider}}.sync-media --sync-to="local" --bucket-path="media" --delete
```


**Database Reset**

To reset your local database from a deployed environment:

```sh
    ({{ cookiecutter.project_app }})$ inv staging pod.get-db-dump --db-var="DATABASE_URL"
```

This will pull down a current snapshot of the database into ``./{{ cookiecutter.project_app }}_database.dump``

Then restore your local database with the file:

```sh
    ({{ cookiecutter.project_app }})$ pg_restore --no-owner --clean --if-exists --dbname {{ cookiecutter.project_app }} < {{ cookiecutter.project_app }}_database.dump
```
