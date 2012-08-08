# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson as json


import geonode.maps.models
import geonode.maps.views

from geonode.layers.models import Layer
from geonode.maps.models import Map

from geonode.utils import default_map_config


class MapsTest(TestCase):
    """Tests geonode.maps app/module
    """

    def setUp(self):
        self.user = 'admin'
        self.passwd = 'admin'

    def tearDown(self):
        pass

    fixtures = ['map_data.json', 'initial_data.json']

    default_abstract = "This is a demonstration of GeoNode, an application \
for assembling and publishing web based maps.  After adding layers to the map, \
use the Save Map button above to contribute your map to the GeoNode \
community." 

    default_title = "GeoNode Default Map"

    # This is a valid map viewer config, based on the sample data provided
    # by andreas in issue 566. -dwins
    viewer_config = """
    {
      "defaultSourceType": "gx_wmssource",
      "about": {
          "title": "Title",
          "abstract": "Abstract"
      },
      "sources": {
        "capra": {
          "url":"http://localhost:8001/geoserver/wms"
        }
      },
      "map": {
        "projection":"EPSG:900913",
        "units":"m",
        "maxResolution":156543.0339,
        "maxExtent":[-20037508.34,-20037508.34,20037508.34,20037508.34],
        "center":[-9428760.8688778,1436891.8972581],
        "layers":[{
          "source":"capra",
          "buffer":0,
          "wms":"capra",
          "name":"base:nic_admin"
        }],
        "keywords":["saving", "keywords"],
        "zoom":7
      }
    }
    """

    viewer_config_alternative = """
    {
      "defaultSourceType": "gx_wmssource",
      "about": {
          "title": "Title2",
          "abstract": "Abstract2"
      },
      "sources": {
        "capra": {
          "url":"http://localhost:8001/geoserver/wms"
        }
      },
      "map": {
        "projection":"EPSG:900913",
        "units":"m",
        "maxResolution":156543.0339,
        "maxExtent":[-20037508.34,-20037508.34,20037508.34,20037508.34],
        "center":[-9428760.8688778,1436891.8972581],
        "layers":[{
          "source":"capra",
          "buffer":0,
          "wms":"capra",
          "name":"base:nic_admin"
        }],
        "zoom":7
      }
    }
    """
    
    perm_spec = {"anonymous":"_none","authenticated":"_none","users":[["admin","map_readwrite"]]}

    def test_map_json(self):
        c = Client()

        # Test that saving a map when not logged in gives 401
        response = c.put("/maps/1/data",data=self.viewer_config,content_type="text/json")
        self.assertEqual(response.status_code, 401)

        c.login(username=self.user, password=self.passwd)
        response = c.put("/maps/1/data",data=self.viewer_config_alternative,content_type="text/json")
        self.assertEqual(response.status_code, 204)

        map_obj = Map.objects.get(id=1)
        self.assertEquals(map_obj.title, "Title2")
        self.assertEquals(map_obj.abstract, "Abstract2")
        self.assertEquals(map_obj.layer_set.all().count(), 1)

    def test_map_save(self):
        """POST /maps -> Test saving a new map"""

        c = Client()

        # Test that saving a map when not logged in gives 401
        response = c.post("/maps/",data=self.viewer_config,content_type="text/json")
        self.assertEqual(response.status_code,401)

        # Test successful new map creation
        c.login(username=self.user, password=self.passwd)
        response = c.post("/maps/",data=self.viewer_config,content_type="text/json")
        self.assertEquals(response.status_code,201)
        map_id = int(response['Location'].split('/')[-1])
        c.logout()

        self.assertEquals(map_id,2)
        map_obj = Map.objects.get(id=map_id)
        self.assertEquals(map_obj.title, "Title")
        self.assertEquals(map_obj.abstract, "Abstract")
        self.assertEquals(map_obj.layer_set.all().count(), 1)
        self.assertEquals(map_obj.keyword_list(), ["keywords", "saving"])

        # Test an invalid map creation request
        c.login(username=self.user, password=self.passwd)
        response = c.post("/maps/",data="not a valid viewer config",content_type="text/json")
        self.assertEquals(response.status_code,400)
        c.logout()

    def test_map_fetch(self):
        """/maps/[id]/data -> Test fetching a map in JSON"""
        map_obj = Map.objects.get(id=1)
        c = Client()
        response = c.get("/maps/%s/data" % map_obj.id)
        self.assertEquals(response.status_code, 200)
        cfg = json.loads(response.content)
        self.assertEquals(cfg["about"]["abstract"], self.default_abstract) 
        self.assertEquals(cfg["about"]["title"], self.default_title) 
        self.assertEquals(len(cfg["map"]["layers"]), 5) 

    def test_map_to_json(self):
        """ Make some assertions about the data structure produced for serialization
            to a JSON map configuration"""
        map_obj = Map.objects.get(id=1)
        cfg = map_obj.viewer_json()
        self.assertEquals(cfg['about']['abstract'], self.default_abstract)
        self.assertEquals(cfg['about']['title'], self.default_title)
        def is_wms_layer(x):
            return cfg['sources'][x['source']]['ptype'] == 'gxp_wmscsource'
        layernames = [x['name'] for x in cfg['map']['layers'] if is_wms_layer(x)]
        self.assertEquals(layernames, ['base:CA',])

    def test_newmap_to_json(self):
        """ Make some assertions about the data structure produced for serialization
            to a new JSON map configuration"""
        response = Client().get("/maps/new/data")
        cfg = json.loads(response.content)
        self.assertEquals(cfg['defaultSourceType'], "gxp_wmscsource")

    def test_map_details(self): 
        """/maps/1 -> Test accessing the map browse view function"""
        map_obj = Map.objects.get(id=1) 
        c = Client()
        response = c.get("/maps/%s" % map_obj.id)
        self.assertEquals(response.status_code,200) 

    def test_new_map_without_layers(self):
        # TODO: Should this test have asserts in it?
        client = Client()
        client.get("/maps/new")

    def test_new_map_with_layer(self):
        client = Client()
        layer = Layer.objects.all()[0]
        client.get("/maps/new?layer=" + layer.typename)

    def test_new_map_with_empty_bbox_layer(self):
        client = Client()
        layer = Layer.objects.all()[0]
        client.get("/maps/new?layer=" + layer.typename)

    def test_ajax_map_permissions(self):
        """Verify that the ajax_layer_permissions view is behaving as expected
        """
        
        # Setup some layer names to work with
        mapid = Map.objects.all()[0].pk
        invalid_mapid = "42"

        c = Client()
        
        url = lambda id: reverse('map_ajax_permissions',args=[id])

        # Test that an invalid layer.typename is handled for properly
        response = c.post(url(invalid_mapid), 
                          data=json.dumps(self.perm_spec),
                          content_type="application/json")
        self.assertEquals(response.status_code, 404) 

        # Test that POST is required
        response = c.get(url(mapid))
        self.assertEquals(response.status_code, 405)
        
        # Test that a user is required to have permissions

        # First test un-authenticated
        response = c.post(url(mapid),
                          data=json.dumps(self.perm_spec),
                          content_type="application/json")
        self.assertEquals(response.status_code, 401)

        # Next Test with a user that does NOT have the proper perms
        logged_in = c.login(username='bobby', password='bob')
        self.assertEquals(logged_in, True)
        response = c.post(url(mapid),
                          data=json.dumps(self.perm_spec),
                          content_type="application/json")
        self.assertEquals(response.status_code, 401)

        # Login as a user with the proper permission and test the endpoint
        logged_in = c.login(username='admin', password='admin')
        self.assertEquals(logged_in, True)

        response = c.post(url(mapid),
                          data=json.dumps(self.perm_spec),
                          content_type="application/json")

        # Test that the method returns 200
        self.assertEquals(response.status_code, 200)

        # Test that the permissions specification is applied


    def test_map_metadata(self):
        """Test that map metadata can be properly rendered
        """
        # first create a map
        c = Client()

        # Test successful new map creation
        c.login(username=self.user, password=self.passwd)
        response = c.post("/maps/",data=self.viewer_config,content_type="text/json")
        self.assertEquals(response.status_code,201)
        map_id = int(response['Location'].split('/')[-1])
        c.logout()
        
        url = '/maps/%s/metadata' % map_id

        # test unauthenticated user to modify map metadata
        response = c.post(url)
        self.assertEquals(response.status_code,302)

        # test a user without metadata modify permission
        c.login(username='norman', password='norman')
        response = c.post(url)
        self.assertEquals(response.status_code, 302)
        c.logout()   

        # Now test with a valid user using GET method
        c.login(username=self.user, password=self.passwd)
        response = c.get(url)
        self.assertEquals(response.status_code, 200)
    
        # Now test with a valid user using POST method
        c.login(username=self.user, password=self.passwd)
        response = c.post(url)
        self.assertEquals(response.status_code, 200)
        
        
        ##############unfinished#########################33


    def test_map_remove(self):
        """Test that map can be properly removed
        """
        # first create a map
        c = Client()

        # Test successful new map creation
        c.login(username=self.user, password=self.passwd)
        response = c.post("/maps/",data=self.viewer_config,content_type="text/json")
        self.assertEquals(response.status_code,201)
        map_id = int(response['Location'].split('/')[-1])
        c.logout()
        
        url = '/maps/%s/remove' % map_id
        
        # test unauthenticated user to remove map
        response = c.post(url)
        self.assertEquals(response.status_code,302)

        # test a user without map removal permission
        c.login(username='norman', password='norman')
        response = c.post(url)
        self.assertEquals(response.status_code, 302)
        c.logout()   

        # Now test with a valid user using GET method
        c.login(username=self.user, password=self.passwd)
        response = c.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Now test with a valid user using POST method, 
        # which removes map and associated layers, and redirects webpage 
        response = c.post(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], 'http://testserver/maps/')
        
        # After removal, map is not existent
        response = c.get(url)
        self.assertEquals(response.status_code, 404)

        #Prepare map object for later test that if it is completely removed
        #map_obj = Map.objects.get(id=1)
        
        ##################work on that####################################
        # Also associated layers are not existent
        ##################work on that####################################
        #self.assertEquals(map_obj.layer_set.all().count(), 0) 
        
     
    def test_map_embed(self):
        """Test that map can be properly embedded
        """
        # first create a map
        c = Client()

        # Test successful new map creation
        c.login(username=self.user, password=self.passwd)
        response = c.post("/maps/",data=self.viewer_config,content_type="text/json")
        self.assertEquals(response.status_code,201)
        map_id = int(response['Location'].split('/')[-1])
        c.logout()
        
        url = '/maps/%s/embed' % map_id
        url_no_id = '/maps/embed/'
        
        # Now test with a map id
        c.login(username=self.user, password=self.passwd)
        response = c.get(url)
        self.assertEquals(response.status_code, 200)
        # Config equals to the map whose id is given
        map_obj = Map.objects.get(id=map_id)
        config_map = map_obj.viewer_json()
        response_config_dict = json.loads(response.context['config'])
        self.assertEquals(config_map['about']['abstract'],response_config_dict['about']['abstract']) 
        self.assertEquals(config_map['about']['title'],response_config_dict['about']['title'])

        # Now test without a map id
        response = c.get(url_no_id)
        self.assertEquals(response.status_code, 200)        
        # Config equals to that of the default map  
        config_default = default_map_config()[0]        
        response_config_dict = json.loads(response.context['config'])
        self.assertEquals(config_default['about']['abstract'],response_config_dict['about']['abstract']) 
        self.assertEquals(config_default['about']['title'],response_config_dict['about']['title'])
        


    def test_map_view(self):
        """Test that map view can be properly rendered
        """
        # first create a map
        c = Client()

        # Test successful new map creation
        c.login(username=self.user, password=self.passwd)
        response = c.post("/maps/",data=self.viewer_config,content_type="text/json")
        self.assertEquals(response.status_code,201)
        map_id = int(response['Location'].split('/')[-1])
        c.logout()
        
        url = '/maps/%s/view' % map_id

        # test unauthenticated user to view map
        response = c.get(url)
        self.assertEquals(response.status_code,200) ##unauthenticated user can still access the map view 

        # test a user without map view permission
        c.login(username='norman', password='norman')
        response = c.get(url)
        self.assertEquals(response.status_code, 200)   ##the user can still access the map view without permission 
        c.logout() 
   
        # Now test with a valid user using GET method
        c.login(username=self.user, password=self.passwd)
        response = c.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Config equals to the map whose id is given
        map_obj = Map.objects.get(id=map_id)
        config_map = map_obj.viewer_json()
        response_config_dict = json.loads(response.context['config'])
        self.assertEquals(config_map['about']['abstract'],response_config_dict['about']['abstract']) 
        self.assertEquals(config_map['about']['title'],response_config_dict['about']['title'])


   
    def test_map_view_js(self):
        """Test that map view js can be properly rendered
        """
        #no url found in urls.py

    def test_new_map_config(self):
        """Test that new map config can be properly assigned 
        """

    """
    def test_map_download(self):
    def test_map_download_check(self):
    def test_maps_search_page(self):
    def test_maps_search(self):
    def test_maps__search(self):
    """
