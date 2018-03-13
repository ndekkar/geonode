#########################################################################
#
# Copyright (C) 2017 OSGeo
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

"""Utilities for enabling OGC WMS remote services in geonode."""

import logging
from urlparse import urlsplit, urljoin
from uuid import uuid4

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from geonode.base.models import Link
from geonode.layers.models import Layer
from geonode.layers.utils import create_thumbnail
from owslib.map import wms111, wms130
from owslib.util import clean_ows_url

from .. import enumerations
from ..enumerations import CASCADED
from ..enumerations import INDEXED
from .. import models

from . import base

logger = logging.getLogger(__name__)


def WebMapService(url,
                  version='1.1.1',
                  xml=None,
                  username=None,
                  password=None,
                  parse_remote_metadata=False,
                  timeout=30,
                  headers=None,
                  proxy_base=None):
    """
    API for Web Map Service (WMS) methods and metadata.

    Currently supports only version 1.1.1 of the WMS protocol.
    """
    '''wms factory function, returns a version specific WebMapService object

    @type url: string
    @param url: url of WFS capabilities document
    @type xml: string
    @param xml: elementtree object
    @type parse_remote_metadata: boolean
    @param parse_remote_metadata: whether to fully process MetadataURL elements
    @param timeout: time (in seconds) after which requests should timeout
    @return: initialized WebFeatureService_2_0_0 object
    '''

    if not proxy_base:
        clean_url = clean_ows_url(url)
        base_ows_url = clean_url
    else:
        (clean_version, proxified_url, base_ows_url) = base.get_proxified_ows_url(
            url, version=version, proxy_base=proxy_base)
        version = clean_version
        clean_url = proxified_url

    if version in ['1.1.1']:
        return (base_ows_url, wms111.WebMapService_1_1_1(clean_url, version=version, xml=xml,
                                                         parse_remote_metadata=parse_remote_metadata,
                                                         username=username, password=password,
                                                         timeout=timeout, headers=headers))
    elif version in ['1.3.0']:
        return (base_ows_url, wms130.WebMapService_1_3_0(clean_url, version=version, xml=xml,
                                                         parse_remote_metadata=parse_remote_metadata,
                                                         username=username, password=password,
                                                         timeout=timeout, headers=headers))
    raise NotImplementedError(
        'The WMS version (%s) you requested is not implemented. Please use 1.1.1 or 1.3.0.' %
        version)


class WmsServiceHandler(base.ServiceHandlerBase,
                        base.CascadableServiceHandlerMixin):
    """Remote service handler for OGC WMS services"""

    service_type = enumerations.WMS

    def __init__(self, url):
        self.proxy_base = urljoin(
            settings.SITEURL, reverse('proxy'))
        (self.url, self.parsed_service) = WebMapService(
            url, proxy_base=self.proxy_base)
        self.indexing_method = (
            INDEXED if self._offers_geonode_projection() else CASCADED)
        # self.url = self.parsed_service.url
        _title = self.parsed_service.identification.title
        self.name = slugify(
            _title if _title else urlsplit(self.url).netloc)[:40]

    def create_cascaded_store(self):
        store = self._get_store(create=True)
        store.capabilitiesURL = self.url
        cat = store.catalog
        cat.save(store)
        return store

    def create_geonode_service(self, owner, parent=None):
        """Create a new geonode.service.models.Service instance

        :arg owner: The user who will own the service instance
        :type owner: geonode.people.models.Profile

        """

        instance = models.Service(
            uuid=str(uuid4()),
            base_url=self.url,
            proxy_base=self.proxy_base,
            type=self.service_type,
            method=self.indexing_method,
            owner=owner,
            parent=parent,
            version=self.parsed_service.identification.version,
            name=self.name,
            title=self.parsed_service.identification.title or self.name,
            abstract=self.parsed_service.identification.abstract or _(
                "Not provided"),
            online_resource=self.parsed_service.provider.url,
        )
        return instance

    def get_keywords(self):
        return self.parsed_service.identification.keywords

    def get_resource(self, resource_id):
        return self.parsed_service.contents[resource_id]

    def get_resources(self):
        """Return an iterable with the service's resources.

        For WMS we take into account that some layers are just logical groups
        of metadata and do not return those.

        """

        contents_gen = self.parsed_service.contents.itervalues()
        return (r for r in contents_gen if not any(r.children))

    def harvest_resource(self, resource_id, geonode_service):
        """Harvest a single resource from the service

        This method will try to create new ``geonode.layers.models.Layer``
        instance (and its related objects too).

        :arg resource_id: The resource's identifier
        :type resource_id: str
        :arg geonode_service: The already saved service instance
        :type geonode_service: geonode.services.models.Service

        """

        layer_meta = self.get_resource(resource_id)
        logger.debug("layer_meta: {}".format(layer_meta))
        if self.indexing_method == CASCADED:
            logger.debug("About to import cascaded layer...")
            geoserver_resource = self._import_cascaded_resource(layer_meta)
            resource_fields = self._get_cascaded_layer_fields(
                geoserver_resource)
            keywords = []
        else:
            resource_fields = self._get_indexed_layer_fields(layer_meta)
            keywords = resource_fields.pop("keywords")
        existance_test_qs = Layer.objects.filter(
            name=resource_fields["name"],
            store=resource_fields["store"],
            workspace=resource_fields["workspace"]
        )
        if existance_test_qs.exists():
            raise RuntimeError(
                "Resource {!r} has already been harvested".format(resource_id))
        # bear in mind that in ``geonode.layers.models`` there is a
        # ``pre_save_layer`` function handler that is connected to the
        # ``pre_save`` signal for the Layer model. This handler does a check
        # for common fields (such as abstract and title) and adds
        # sensible default values
        geonode_layer = Layer(
            owner=geonode_service.owner,
            service=geonode_service,
            uuid=str(uuid4()),
            **resource_fields
        )
        geonode_layer.full_clean()
        geonode_layer.save()
        geonode_layer.keywords.add(*keywords)
        geonode_layer.set_default_permissions()
        self._create_layer_service_link(geonode_layer)
        self._create_layer_legend_link(geonode_layer)
        self._create_layer_thumbnail(geonode_layer)

    def has_resources(self):
        return True if len(self.parsed_service.contents) > 1 else False

    def _create_layer_thumbnail(self, geonode_layer):
        """Create a thumbnail with a WMS request."""
        params = {
            "service": "WMS",
            "version": self.parsed_service.version,
            "request": "GetMap",
            "layers": geonode_layer.alternate.encode('utf-8'),
            "bbox": geonode_layer.bbox_string,
            "srs": "EPSG:4326",
            "width": "200",
            "height": "150",
            "format": "image/png",
        }
        kvp = "&".join("{}={}".format(*item) for item in params.items())
        thumbnail_remote_url = "{}?{}".format(
            geonode_layer.service.service_url, kvp)
        logger.debug("thumbnail_remote_url: {}".format(thumbnail_remote_url))
        create_thumbnail(
            instance=geonode_layer,
            thumbnail_remote_url=thumbnail_remote_url,
            thumbnail_create_url=None,
            check_bbox=False,
            overwrite=True
        )

    def _create_layer_legend_link(self, geonode_layer):
        """Get the layer's legend and save it locally

        Regardless of the service being INDEXED or CASCADED we're always
        creating the legend by making a request directly to the original
        service.

        """

        params = {
            "service": "WMS",
            "version": self.parsed_service.version,
            "request": "GetLegendGraphic",
            "format": "image/png",
            "width": 20,
            "height": 20,
            "layer": geonode_layer.name,
            "legend_options": (
                "fontAntiAliasing:true;fontSize:12;forceLabels:on")
        }
        kvp = "&".join("{}={}".format(*item) for item in params.items())
        legend_url = "{}?{}".format(
            geonode_layer.service.service_url, kvp)
        logger.debug("legend_url: {}".format(legend_url))
        Link.objects.get_or_create(
            resource=geonode_layer.resourcebase_ptr,
            url=legend_url,
            defaults={
                "extension": 'png',
                "name": 'Legend',
                "url": legend_url,
                "mime": 'image/png',
                "link_type": 'image',
            }
        )

    def _create_layer_service_link(self, geonode_layer):
        Link.objects.get_or_create(
            resource=geonode_layer.resourcebase_ptr,
            url=geonode_layer.ows_url,
            defaults={
                "extension": "html",
                "name": "OGC {}: {} Service".format(
                    geonode_layer.service.type,
                    geonode_layer.store
                ),
                "url": geonode_layer.ows_url,
                "mime": "text/html",
                "link_type": "OGC:{}".format(geonode_layer.service.type),
            }
        )

    def _get_cascaded_layer_fields(self, geoserver_resource):
        name = geoserver_resource.name
        workspace = geoserver_resource.workspace.name
        store = geoserver_resource.store
        bbox = geoserver_resource.latlon_bbox
        return {
            "name": name,
            "workspace": workspace,
            "store": store.name,
            "typename": "{}:{}".format(workspace, name),
            "storeType": "remoteStore",  # store.resource_type,
            "title": geoserver_resource.title,
            "abstract": geoserver_resource.abstract,
            "bbox_x0": bbox[0],
            "bbox_x1": bbox[1],
            "bbox_y0": bbox[2],
            "bbox_y1": bbox[3],
        }

    def _get_indexed_layer_fields(self, layer_meta):
        bbox = layer_meta.boundingBoxWGS84
        return {
            "name": layer_meta.name,
            "store": self.name,
            "storeType": "remoteStore",
            "workspace": "remoteWorkspace",
            "typename": layer_meta.name,
            "title": layer_meta.title,
            "abstract": layer_meta.abstract,
            "bbox_x0": bbox[0],
            "bbox_x1": bbox[2],
            "bbox_y0": bbox[1],
            "bbox_y1": bbox[3],
            "keywords": [keyword[:100] for keyword in layer_meta.keywords],
        }

    def _get_store(self, create=True):
        """Return the geoserver store associated with this service.

        The store may optionally be created if it doesn't exist already.
        Store is assumed to be (and created) named after the instance's name
        and belongs to the default geonode workspace for cascaded layers.

        """

        workspace = base.get_geoserver_cascading_workspace(create=create)
        cat = workspace.catalog
        store = cat.get_store(self.name, workspace=workspace)
        logger.debug("name: {}".format(self.name))
        logger.debug("store: {}".format(store))
        if store is None and create:  # store did not exist. Create it
            store = cat.create_wmsstore(
                name=self.name,
                workspace=workspace,
                user=cat.username,
                password=cat.password
            )
        return store

    def _import_cascaded_resource(self, layer_meta):
        """Import a layer into geoserver in order to enable cascading."""
        store = self._get_store(create=False)
        cat = store.catalog
        workspace = store.workspace
        layer_resource = cat.get_resource(layer_meta.id, store, workspace)
        if layer_resource is None:
            layer_resource = cat.create_wmslayer(
                workspace, store, layer_meta.id)
            layer_resource.projection = getattr(
                settings, "DEFAULT_MAP_CRS", "EPSG:3857")
            # Do not use the geoserver.support.REPROJECT enumeration until
            # https://github.com/boundlessgeo/gsconfig/issues/174
            # has been fixed
            layer_resource.projection_policy = "REPROJECT_TO_DECLARED"
            cat.save(layer_resource)
            if layer_resource is None:
                raise RuntimeError("Could not cascade resource {!r} through "
                                   "geoserver".format(layer_meta))
        else:
            logger.info("Layer {} is already present. Skipping...".format(
                layer_meta.id))
        return layer_resource

    def _offers_geonode_projection(self):
        geonode_projection = getattr(settings, "DEFAULT_MAP_CRS", "EPSG:3857")
        first_layer = list(self.get_resources())[0]
        return geonode_projection in first_layer.crsOptions


class GeoNodeServiceHandler(WmsServiceHandler):
    """Remote service handler for OGC WMS services"""

    # TODO: Parse Layers Details from
    #
    #     http://<geonode_base>/api/layers/?name=actualevap
    #
    #     {
    #     	"geonode_version": "2.9.dev20180220135741",
    #     	"meta": {
    #     		"limit": 1000,
    #     		"next": null,
    #     		"offset": 0,
    #     		"previous": null,
    #     		"total_count": 1
    #     	},
    #     	"objects": [{
    #     		"abstract": "This layer represents the actual evapotranspiration in 2006, ...",
    #     		"alternate": "geonode:actualevap",
    #     		"category__gn_description": "Ecohydrology",
    #     		"csw_type": "dataset",
    #     		"csw_wkt_geometry": "POLYGON((-180.0000000000 -59.4842793000,-...",
    #     		"date": "2017-08-17T09:34:00",
    #     		"default_style": "/api/styles/232/",
    #     		"detail_url": "/layers/geonode:actualevap",
    #     		"geogig_link": null,
    #     		"group": "IHP-Theme6-Water-education",
    #     		"group_name": "Theme 6: Water education",
    #     		"has_time": false,
    #     		"id": 901,
    #     		"is_approved": true,
    #     		"is_published": true,
    #     		"name": "actualevap",
    #     		"owner__username": "najet.guefradj",
    #     		"owner_name": "Najet Guefradj",
    #     		"popular_count": 17,
    #     		"rating": 0,
    #     		"resource_uri": "/api/layers/901/",
    #     		"share_count": 0,
    #     		"srid": "EPSG:4326",
    #     		"supplemental_information": "UNSD Environmental Indicators disseminate ...",
    #     		"thumbnail_url": "http://ihp-wins.unesco.org/uploaded/thumbs/layer-...",
    #     		"title": "Actual evapotranspiration in 2006",
    #     		"typename": "geonode:actualevap",
    #     		"uuid": "ceca70ee-b88d-11e7-bdb3-005056062634"
    #     	}]
    #     }

    service_type = enumerations.GN_WMS

    def __init__(self, url):
        self.proxy_base = urljoin(
            settings.SITEURL, reverse('proxy'))

        url = self._probe_geonode_wms(url)

        (self.url, self.parsed_service) = WebMapService(
            url, proxy_base=self.proxy_base)
        self.indexing_method = (
            INDEXED if self._offers_geonode_projection() else CASCADED)
        # self.url = self.parsed_service.url
        _title = self.parsed_service.identification.title
        self.name = slugify(
            _title if _title else urlsplit(self.url).netloc)[:40]

    def _probe_geonode_wms(self, raw_url):
        import json
        from httplib import HTTPConnection, HTTPSConnection

        url = urlsplit(raw_url)

        if url.scheme == 'https':
            conn = HTTPSConnection(url.hostname, url.port)
        else:
            conn = HTTPConnection(url.hostname, url.port)
        conn.request('GET', '/api/ows_endpoints/', '', {})
        response = conn.getresponse()
        content = response.read()
        status = response.status
        content_type = response.getheader("Content-Type", "text/plain")

        # NEW-style OWS Enabled GeoNode
        if status == 200 and 'application/json' == content_type:
            try:
                _json_obj = json.loads(content)
                if 'data' in _json_obj:
                    data = _json_obj['data']
                    for ows_endpoint in data:
                        if 'OGC:WMS' == ows_endpoint['type']:
                            return ows_endpoint['url'] + '?' + url.query
            except BaseException:
                pass

        # OLD-style not OWS Enabled GeoNode
        _url = "%s://%s/geoserver/wms" % (url.scheme, url.netloc)
        return _url


def _get_valid_name(proposed_name):
    """Return a unique slug name for a service"""
    slug_name = slugify(proposed_name)
    name = slug_name
    if len(slug_name) > 40:
        name = slug_name[:40]
    return name
