from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from apps.search import views as search_views
{% if cookiecutter.project_type == "wagtail" -%}
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
{% endif %}

urlpatterns = [
    path("search/", search_views.search, name="search"),
    path("admin/", admin.site.urls),
]

{% if cookiecutter.project_type == "wagtail" %}
urlpatterns += [
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]
{% endif %}

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
