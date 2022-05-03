from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from apps.client_onboarding import views as client_views

{% if cookiecutter.project_type == "django" -%}
from .views import HomePageView
{%endif %}

{% if cookiecutter.project_type == "wagtail" -%}
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from apps.search import views as search_views
{% endif %}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("caktus-portal/", client_views.list_links),
    # This line will be deleted or modified once the project has a different homepage
    path("", client_views.list_links),
]

{% if cookiecutter.project_type == "wagtail" %}
urlpatterns += [
    path("search/", search_views.search, name="search"),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]
{% endif %}

urlpatterns += [
{% if cookiecutter.project_type == "django" -%}
    path("", HomePageView.as_view(), name='index'),
{% endif %}
{% if cookiecutter.project_type == "wagtail" -%}
    path("", include(wagtail_urls)),
{% endif %}
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
