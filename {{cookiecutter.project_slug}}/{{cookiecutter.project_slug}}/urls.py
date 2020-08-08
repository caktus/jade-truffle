from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from apps.{{ cookiecutter.primary_app }} import views as primary_views
from apps.search import views as search_views
{% if cookiecutter.project_type == "wagtail" %}
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
{% endif%}


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^search/$", search_views.search, name="search"),
]

{% if cookiecutter.project_type == "wagtail" %}
# Wagtail
urlpatterns += [
    url(r"^cms/", include(wagtailadmin_urls)),
    url(r"^documents/", include(wagtaildocs_urls)),
]
{% endif %}

if settings.ENVIRONMENT == "staging":
    urlpatterns += [path("error/", primary_views.ExceptionView.as_view())]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Expose 404 and 500 templates for testing
    urlpatterns += [
        path("404/", TemplateView.as_view(template_name="404.html")),
        path("500/", TemplateView.as_view(template_name="500.html")),
    ]

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

handler404 = "apps.{{ cookiecutter.primary_app }}.views.handler404"
handler500 = "apps.{{ cookiecutter.primary_app }}.views.handler500"

{% if cookiecutter.project_type == "wagtail" %}
urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
]
{% endif %}