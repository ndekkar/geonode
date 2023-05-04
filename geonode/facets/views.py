import logging
from urllib.parse import urlencode

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes

from django.http import HttpResponseNotFound, JsonResponse
from django.urls import reverse

from geonode.base.models import ResourceBase
from geonode.facets.models import FacetProvider, DEFAULT_FACET_PAGE_SIZE, facet_registry
from geonode.security.utils import get_visible_resources

PARAM_PAGE = "page"
PARAM_PAGE_SIZE = "page_size"
PARAM_LANG = "lang"
PARAM_ADD_LINKS = "add_links"
PARAM_INCLUDE_TOPICS = "include_topics"
PARAM_TOPIC_CONTAINS = "topic_contains"

logger = logging.getLogger(__name__)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def list_facets(request, **kwargs):
    lang, lang_requested = _resolve_language(request)
    add_links = _resolve_boolean(request, PARAM_ADD_LINKS, False)
    include_topics = _resolve_boolean(request, PARAM_INCLUDE_TOPICS, False)

    facets = []

    for provider in facet_registry.get_providers():
        logger.debug("Fetching data from provider %r", provider)
        info = provider.get_info(lang=lang)
        if add_links:
            link_args = {PARAM_ADD_LINKS: True}
            if lang_requested:  # only add lang param if specified in current call
                link_args[PARAM_LANG] = lang
            info["link"] = f"{reverse('get_facet', args=[info['name']])}?{urlencode(link_args)}"

        if include_topics:
            info["topics"] = _get_topics(provider, queryset=_prefilter_topics(request), lang=lang)

        facets.append(info)

    logger.debug("Returning facets %r", facets)
    return JsonResponse({"facets": facets})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_facet(request, facet):
    logger.debug("get_facet -> %r for user '%r'", facet, request.user.username)

    # retrieve provider for the requested facet
    provider: FacetProvider = facet_registry.get_provider(facet)
    if not provider:
        return HttpResponseNotFound()

    # parse some query params
    lang, lang_requested = _resolve_language(request)
    add_link = _resolve_boolean(request, PARAM_ADD_LINKS, False)
    topic_contains = request.GET.get(PARAM_TOPIC_CONTAINS, None)
    page = int(request.GET.get(PARAM_PAGE, 0))
    page_size = int(request.GET.get(PARAM_PAGE_SIZE, DEFAULT_FACET_PAGE_SIZE))

    info = provider.get_info(lang)

    qs = _prefilter_topics(request)
    topics = _get_topics(
        provider, queryset=qs, page=page, page_size=page_size, lang=lang, topic_contains=topic_contains
    )

    if add_link:
        exist_prev = page > 0
        exist_next = topics["total"] > (page + 1) * page_size
        link = reverse("get_facet", args=[info["name"]])
        for exist, link_name, p in (
            (exist_prev, "prev", page - 1),
            (exist_next, "next", page + 1),
        ):
            link_param = {PARAM_PAGE: p, PARAM_PAGE_SIZE: page_size, PARAM_LANG: lang, PARAM_ADD_LINKS: True}
            if lang_requested:  # only add lang param if specified in current call
                link_param[PARAM_LANG] = lang
            if topic_contains:
                link_param[PARAM_TOPIC_CONTAINS] = topic_contains
            info[link_name] = f"{link}?{urlencode(link_param)}" if exist else None

    if topic_contains:
        # in the payload let's rmb this is a filtered output
        info["topic_contains"] = topic_contains

    info["topics"] = topics

    return JsonResponse(info)


def _get_topics(
    provider,
    queryset,
    page: int = 0,
    page_size: int = DEFAULT_FACET_PAGE_SIZE,
    lang: str = "en",
    topic_contains: str = None,
):
    start = page * page_size
    end = start + page_size

    cnt, items = provider.get_facet_items(queryset, start=start, end=end, lang=lang, topic_contains=topic_contains)

    return {"page": page, "page_size": page_size, "start": start, "total": cnt, "items": items}


def _prefilter_topics(request):
    """
    Perform some prefiltering on resources, such as
      - auth visibility
      - filtering by other facets already applied
    :param request:
    :return: a QuerySet on ResourceBase
    """
    return get_visible_resources(ResourceBase.objects, request.user)


def _resolve_language(request) -> (str, bool):
    """
    :return: the resolved language, a boolean telling if the language was requested
    """
    # first try with an explicit request using params
    if lang := request.GET.get(PARAM_LANG, None):
        return lang, True
    # 2nd try: use LANGUAGE_CODE
    return request.LANGUAGE_CODE.split("-")[0], False


def _resolve_boolean(request, name, fallback=None):
    """
    Parse boolean query params
    """
    val = request.GET.get(name, None)
    if val is None:
        return fallback

    val = val.lower()
    if val.startswith("t") or val.startswith("y") or val == "1":
        return True
    elif val.startswith("f") or val.startswith("n") or val == "0":
        return False
    else:
        return fallback
