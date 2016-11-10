from tastypie.resources import ModelResource
from tastypie import fields
from taggit.models import Tag

from geonode.maps.models import Layer, LayerCategory


class LayerCategoryResource(ModelResource):

    class Meta:
        queryset = LayerCategory.objects.all()
        allowed_methods = ['get', ]
        fields = ['name', 'description']


class TagResource(ModelResource):

    class Meta:
        queryset = Tag.objects.all()
        fields = ['name', ]


class LayerResource(ModelResource):

    topic_category = fields.CharField(readonly=True)
    owner_username = fields.CharField(readonly=True)
    is_public = fields.BooleanField(readonly=True)
    keywords = fields.ToManyField(TagResource, 'keywords', full = True)

    def dehydrate_topic_category(self, bundle):
        return bundle.obj.topic_category.title

    def dehydrate_owner_username(self, bundle):
        return bundle.obj.owner.username

    def dehydrate_is_public(self, bundle):
        return bundle.request.user.has_perm('maps.view_layer', obj=bundle.obj)

    class Meta:
        queryset = Layer.objects.all()
        allowed_methods = ['get', ]
        ordering = ['last_modified', ]
        fields = ['abstract', 'bbox', 'date', 'date_type', 'is_public', 'keywords',
            'last_modified', 'name', 'owner_username', 'srs', 'temporal_extent_end',
            'temporal_extent_start', 'title', 'topic_category', 'typename', 'uuid',
        ]
