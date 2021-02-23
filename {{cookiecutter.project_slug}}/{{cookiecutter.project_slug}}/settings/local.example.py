from {{ cookiecutter.project_slug }}.settings.dev import *  # noqa


# Override settings here
INSTALLED_APPS += (
    # 'debug_toolbar',
    # show the styleguide in /cms/styleguide:
    "django_extensions",
)

ALLOWED_HOSTS = ["localhost", ""]
