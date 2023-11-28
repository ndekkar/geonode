#########################################################################
#
# Copyright (C) 2019 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
from django.conf.urls import url, include

from .views import (
    DatasetsAutocomplete,
    resource_clone,
    RegionAutocomplete,
    ThesaurusAvailable,
    OwnerRightsRequestView,
    ResourceBaseAutocomplete,
    HierarchicalKeywordAutocomplete,
    ThesaurusKeywordLabelAutocomplete,
    LinkedResourcesAutocomplete,
)


urlpatterns = [
    url(
        r"^autocomplete_response/$",
        ResourceBaseAutocomplete.as_view(),
        name="autocomplete_base",
    ),
    url(
        r"^autocomplete_linked_resource/$",
        LinkedResourcesAutocomplete.as_view(),
        name="autocomplete_linked_resource",
    ),
    url(
        r"^autocomplete_region/$",
        RegionAutocomplete.as_view(),
        name="autocomplete_region",
    ),
    url(
        r"^autocomplete_hierachical_keyword/$",
        HierarchicalKeywordAutocomplete.as_view(),
        name="autocomplete_hierachical_keyword",
    ),
    url(
        r"^thesaurus_available",
        ThesaurusAvailable.as_view(),
        name="thesaurus_available",
    ),
    url(
        r"^thesaurus_autocomplete/$",
        ThesaurusKeywordLabelAutocomplete.as_view(),
        name="thesaurus_autocomplete",
    ),
    url(
        r"^datasets_autocomplete/$",
        DatasetsAutocomplete.as_view(),
        name="datasets_autocomplete",
    ),
    url(
<<<<<<< HEAD
        r"^resource_rights/(?P<pk>\d+)$",
=======
        r'^datasets_autocomplete/$',
        DatasetsAutocomplete.as_view(),
        name='datasets_autocomplete',
    ),
    url(
        r'^resource_rights/(?P<pk>\d+)$',
>>>>>>> fedc0bf0f72966b9853f8c33aa2737899fa050e6
        OwnerRightsRequestView.as_view(),
        name="owner_rights_request",
    ),
    url(
        r"^resource_clone/?$",
        resource_clone,
        name="resource_clone",
    ),
    url(r"^", include("geonode.base.api.urls")),
]
