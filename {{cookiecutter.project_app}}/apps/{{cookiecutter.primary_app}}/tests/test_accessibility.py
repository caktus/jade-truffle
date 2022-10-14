{% if cookiecutter.project_type == 'django' and cookiecutter.testing_type == 'django' %}
from axe_selenium_python import Axe
from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from django.shortcuts import reverse
from django.test import override_settings
{% elif cookiecutter.project_type == 'django' and cookiecutter.testing_type == 'pytest' %}
import pytest
from axe_selenium_python import Axe
from selenium import webdriver

from django.shortcuts import reverse
{% elif cookiecutter.project_type == 'wagtail' and cookiecutter.testing_type == 'django' %}
from axe_selenium_python import Axe
from selenium import webdriver
from wagtail.core.models import Page

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from django.shortcuts import reverse
from django.test import override_settings
{% elif cookiecutter.project_type == 'wagtail' and cookiecutter.testing_type == 'pytest' %}
import pytest
from axe_selenium_python import Axe
from selenium import webdriver
import wagtail_factories

from wagtail.core.models import Locale, Page
from wagtail.models.sites import Site
{% endif %}


{% if cookiecutter.testing_type == 'django' %}
@override_settings(
    STATICFILES_STORAGE="whitenoise.storage.CompressedStaticFilesStorage"
)
class TestAccessibility(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        # Set self.driver to be a headless Firefox browser.
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def close_db_sessions(self, conn):
        """
        Close all database sessions.
        Note: this should automatically happen on teardown, but for some reason
        using Selenium with LiveServerTestCase doesn't automatically close all
        database sessions on teardown, so this method does so explicitly.
        Code based on:
        stackoverflow.com/questions/53323775/database-still-in-use-after-a-selenium-test-in-django
        """
        close_sessions_query = """
            SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE
                datname = current_database() AND
                pid <> pg_backend_pid();
        """
        with conn.cursor() as cursor:
            try:
                cursor.execute(close_sessions_query)
            except OperationalError:
                pass

    def test_pages(self):
        """Run accessibility tests on pages of the site."""
        {% if cookiecutter.project_type == 'django' %}
        subtests = (
            # page_name, page_url
            ("homepage", reverse("home")),
        )
        {% elif cookiecutter.project_type == 'wagtail' %}
        # Find the homepage.
        homepage = None
        for page in Page.objects.all():
            if page.is_site_root():
                homepage = page

        subtests = (
            # page_name, page_url
            ("homepage", homepage.url),
        )
        {% endif %}
        for page_name, page_url in subtests:
            with self.subTest(page_name=page_name, page_url=page_url):
                url = self.live_server_url + page_url
                self.driver.get(url)

                axe = Axe(self.driver)
                # Inject axe-core javascript into page.
                axe.inject()
                # Run axe accessibility checks.
                results = axe.run()

                # If there are violations, then write them to a file
                if len(results["violations"]) > 0:
                    violations_filename = (
                        f"apps/{{cookiecutter.primary_app}}/tests/violations_{page_name}.json"
                    )
                    axe.write_results(results["violations"], violations_filename)

                # Assert that there are no violations, or print out the titles
                # of each of the violations.
                violations_titles_list = [
                    result["description"] for result in results["violations"]
                ]
                violations_titles_str = "\n".join(
                    [f"  {title}" for title in violations_titles_list]
                )
                error_msg = (
                    f"\n\nAccessibility violations:\n{violations_titles_str}\n\n"
                    f"Violation results have been written to {violations_filename}"
                )
                self.assertEqual(0, len(violations_titles_list), error_msg)

    def tearDown(self):
        # Quit the browser.
        self.driver.quit()

        # Close all database connections (if they're still open).
        for alias in connections:
            connections[alias].close()
            self.close_db_sessions(connections[alias])

        super().tearDown()
{% elif cookiecutter.testing_type == 'pytest' %}

{% if cookiecutter.project_type == 'wagtail' %}
@pytest.fixture
def homepage():
    """Create a homepage."""
    # Create the homepage.
    locale = Locale.objects.create()
    homepage = wagtail_factories.PageFactory(locale=locale)
    # Make sure that the homepage is the root page of the the current Site.
    site = Site.objects.first()
    if site:
        site.root_page = homepage
        site.save()
    else:
        site = Site.objects.create(root_page=homepage)
    return homepage


@pytest.fixture
def pages_for_accessibility_tests(homepage):
    """Create Pages for accessibility tests."""
    # Create other pages for accessibility tests here.

    # Return a dictionary of page_name: page. For example,
    # {"homepage": homepage, "pictures_page": pictures_page}. The keys of this
    # dictionary should match the page_name values in the test_accessibility_on_pages().
    return {"homepage": homepage}


@pytest.fixture
def page_url(request, pages_for_accessibility_tests):
    """Return the URL for a Wagtail Page."""
    # Get the Page for the request.param (which is the page_name, and should match
    # a key from the pages_for_accessibility_tests).
    page = pages_for_accessibility_tests.get(request.param)
    return page.url
{% endif %}

{% if cookiecutter.project_type == 'django' %}
@pytest.mark.parametrize("page_name,page_url", [("homepage", reverse("home"))])
{% elif cookiecutter.project_type == 'wagtail' %}
@pytest.mark.parametrize("page_name,page_url", [("homepage", "homepage")], indirect=["page_url"])
{% endif %}
def test_accessibility_on_pages(
    live_server, django_db_serialized_rollback, settings, page_name, page_url
):
    """Run accessibility tests on pages of the site."""
    # Set STATICFILES_STORAGE to not use unique suffixes on static files, so they
    # can be found properly.
    settings.STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

    # Set driver to be a headless Firefox browser.
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    url = live_server.url + page_url
    driver.get(url)

    axe = Axe(driver)
    # Inject axe-core javascript into page.
    axe.inject()
    # Run axe accessibility checks.
    results = axe.run()

    # If there are violations, then write them to a file
    if len(results["violations"]) > 0:
        violations_filename = (
            f"apps/{{cookiecutter.primary_app}}/tests/violations_{page_name}.json"
        )
        axe.write_results(results["violations"], violations_filename)

    # Assert that there are no violations, or print out the titles
    # of each of the violations.
    violations_titles_list = [result["description"] for result in results["violations"]]
    violations_titles_str = "\n".join(
        [f"  {title}" for title in violations_titles_list]
    )
    error_msg = (
        f"\n\nAccessibility violations:\n{violations_titles_str}\n\n"
        f"Violation results have been written to {violations_filename}"
    )
    assert 0 == len(violations_titles_list), error_msg

    # Quit the browser.
    driver.quit()
{% endif %}
