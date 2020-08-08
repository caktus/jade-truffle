import json
from itertools import chain

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt


def _get_search_results(search_query):
    page_results = Page.objects.live().search(search_query, operator="or").annotate_score("_score")
    document_results = (
        get_document_model().objects.search(search_query, operator="or").annotate_score("_score")
    )
    search_results = list(chain(page_results, document_results))
    search_results.sort(key=lambda x: x._score, reverse=True)
    return search_results


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = _get_search_results(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, settings.SEARCH_PAGE_SIZE)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/search.html",
        {"search_query": search_query, "search_results": search_results},
    )