# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
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

from django.conf.urls.defaults import patterns, url

js_info_dict = {
    'packages': ('geonode.documents',),
}

urlpatterns = patterns('geonode.documents.views',
    url(r'^$', 'document_list', name='documents_browse'),
    url(r'^tag/(?P<slug>[-\w]+?)/$', 'document_tag', name='document_browse_tag'),
    url(r'^(?P<docid>\d+)/?$', 'document_detail', name='document_detail'),
    url(r'^(?P<docid>\d+)/download/?$', 'document_download', name='document_download'),
    url(r'^(?P<docid>\d+)/replace$', 'document_replace',
        name="document_replace"),
    url(r'^(?P<docid>\d+)/remove$', 'document_remove',
        name="document_remove"),
    url(r'^upload/?$', 'document_upload', name='document_upload'),
    url(r'^search/?$', 'document_search_page', name='document_search_page'),
    url(r'^(?P<docid>\d+)/permissions$', 'document_permissions', name='document_permissions'),
    url(r'^(?P<docid>\d+)/metadata$', 'document_metadata', name='document_metadata'),
)