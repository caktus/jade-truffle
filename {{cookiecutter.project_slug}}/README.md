# {{ cookiecutter.project_name }}


## ✏️ **Develop**
To begin you should have the following applications installed on your local development system:

- Python >= 3.8
- NodeJS == 12.16.x
- npm == 6.14.x (comes with node 10)
- [nvm](https://github.com/nvm-sh/nvm/blob/master/README.md) is not strictly _required_, but will almost certainly be necessary unless you just happen to have Node.js 12.x installed on your machine.
- [pip](http://www.pip-installer.org/) >= 20
- [virtualenv](http://www.virtualenv.org/) >= 1.10
- [virtualenvwrapper](http://pypi.python.org/pypi/virtualenvwrapper) >= 3.0
- Postgres >= 12
- git >= 2.26
- [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)


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
{%load sass_tags %}
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


### 💪 **Setup Manually**

**1. Get the project**

First clone the repository from Github and switch to the new directory:

```linux
    $ git clone git@github.com:caktus{{ cookiecutter.project_slug }}.git
    $ cd {{ cookiecutter.project_slug }}
```

**2. Set up venv**

Next, set up your virtual environment:

```linux
    # Check that you have python3 >= 3.8 installed
    $ which python3

    # Create the virtual environment, either with mkvirtualenv:
    $ mkvirtualenv {{ cookiecutter.project_slug }} -p `which python3`

    # or directly (if your system is set up differently than mkvirtualenv assumes):
    $ python3 -m virtualenv ~/.virtualenvs {{ cookiecutter.project_slug }}
    $ ln -s ~/.virtualenvs {{ cookiecutter.project_slug }}/bin/activate .venv
    $ source .venv
```


**3. Install dependencies**

``nvm`` is preferred for managing Node versions and ``.nvmrc`` contains the
specific Node version for this project. To install the correct (and latest)
Node version run:

```sh
    ({{ cookiecutter.project_slug }})$ nvm install
```

Now install the project Node packages with ``npm``:

```sh
    ({{ cookiecutter.project_slug }})$ npm install
```

Install Python dependencies with:

```linux
    ({{ cookiecutter.project_slug }})$ make setup
```

NOTE: This project uses ``pip-tools``. If the dependency `.txt` files need to be
updated:

```sh
    ({{ cookiecutter.project_slug }})$ make update_requirements setup
```

NOTE 2: During a development cycle if a developer needs to add subtract or modify the requirements of the project, the 
workflow is to:

1) Make the change in the ``*.in`` requirement file
2) run ``make update_requirements``
3) commit both ``*.in`` file(s) and the ``*.txt`` file(s) generated


**4. Pre-commit**

pre-commit is used to enforce a variety of community standards. Travis runs it,
so it's useful to setup the pre-commit hook to catch any issues before pushing
to GitHub.

To install, run:

```linux
    ({{ cookiecutter.project_slug }})$ pre-commit install
```


**5. Set up local env variables**

Next, we'll set up our local environment variables. We use
[django-dotenv](https://github.com/jpadilla/django-dotenv) to help with this. It
reads environment variables located in a file named `.env` in the top level
directory of the project. The only variable we need to start is
`DJANGO_SETTINGS_MODULE`:

```linux
    ({{ cookiecutter.project_slug }})$ cp {{ cookiecutter.project_slug }}/settings/local.example.py {{ cookiecutter.project_slug }}/settings/local.py
    ({{ cookiecutter.project_slug }})$ echo "DJANGO_SETTINGS_MODULE={{ cookiecutter.project_slug }}.settings.local" > .env
```


**6. Database**

The setup for local development assumes that you will be working with dockerized
services.

First add the following line to your .env file:

```sh
({{ cookiecutter.project_slug }})$ echo "DATABASE_URL=postgres://postgres@127.0.0.1:{{ cookiecutter.postgres_port }}/{{ cookiecutter.project_slug }}" >> .env
```

The `docker-compose.yml` sets up environment variables in a file, ``.postgres``.
To use the Docker setup, add these lines to that file:

```sh
    POSTGRES_DB={{ cookiecutter.project_slug }}
    POSTGRES_HOST_AUTH_METHOD=trust
```

If you want to connect to the database from your host machine, export the
following shell environment variables:

```sh
    export PGHOST=127.0.0.1
    export PGPORT={{ cookiecutter.postgres_port }}
    export PGUSER=postgres
    export PGDATABASE={{ cookiecutter.project_slug }}
```


**7. Migrate and run**

```linux
    ({{ cookiecutter.project_slug }})$ docker-compose up -d
    ({{ cookiecutter.project_slug }})$ python manage.py migrate
    ({{ cookiecutter.project_slug }})$ make run-dev
```

After initial setup the development server should be run using ``make run-dev`` this will remove any deployment containers hanging around and setup using local sources and database.

**8. Run tests**

{{ cookiecutter.project_slug }} uses pytest as a test runner.


```sh
    ({{ cookiecutter.project_slug }})$ make run-tests
```

**9. Reset Media and Database**

{{ cookiecutter.project_slug }} uses invoke for interactions with the deployed environments.  

**Media Reset**


From time to time it may become necessary to sync your local media tree with either production or staging.

The basic command for resetting your local media is this:


```sh
    ({{ cookiecutter.project_slug }})$ inv staging reset-local-media
```

If you wish to make sure you need to reset you can issue the command with a ``dry-run`` argument.


```sh
    ({{ cookiecutter.project_slug }})$ inv staging reset-local-media --dry-run
```

If you wish to clean out your local media tree before reset you can issue the command with a ``clean-local`` argument.


```sh
    ({{ cookiecutter.project_slug }})$ inv staging reset-local-media --clean-local
```


**Database Reset**

If you need to reset your local database from a deployed environment there is an invoke command for that as well.

The basic command for resetting your local database is this:


```sh
    ({{ cookiecutter.project_slug }})$ inv staging reset-local-db
```

If you have already retrieved a database file, for example from a backup server, you can restore that dump using the
``dump-file`` argument.


```sh
    ({{ cookiecutter.project_slug }})$ inv reset-local-db --dump-file="<PATH_TO_BACKUPFILE>"
```
