"""Models for the ``WaterProof Intake`` app."""

from django.conf import settings
from django.db import models
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from geonode.waterproof_nbs_ca.models import Countries
from geonode.waterproof_nbs_ca.models import Currency


class City(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    def __str__(self):
        return "%s" % self.name


class UserCosts(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    value = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Value')
    )


class SystemCosts(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    value = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Extraction value')
    )


class CostFunctionsProcess(models.Model):

    symbol = models.CharField(
        max_length=5,
        verbose_name=_('Symbol')
    )

    categorys = models.CharField(
        max_length=100,
        verbose_name=_('Categorys')
    )

    energy = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Energy')
    )

    labour = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Labour')
    )

    mater_equipment = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Materials equipment')
    )

    function=models.CharField(
        max_length=1000,
        verbose_name=_('Function')
    )

    function_name=models.CharField(
        max_length=250,
        verbose_name=_('Function name')
    )

    function_description=models.CharField(
        max_length=250,
        verbose_name=_('Function description')
    )


class ProcessEfficiencies(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name=_('Name')
    )

    unitary_process = models.CharField(
        max_length=100,
        verbose_name=_('Unitary process')
    )

    symbol = models.CharField(
        max_length=100,
        verbose_name=_('Symbol')
    )

    categorys = models.CharField(
        max_length=100,
        verbose_name=_('Categorys')
    )

    normalized_category = models.CharField(
        max_length=100,
        verbose_name=_('Normalized category')
    )

    minimal_sediment_perc = models.IntegerField(
        default=0,
        verbose_name=_('Minimal sediment')
    )

    predefined_sediment_perc = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Predefined sediment')
    )

    maximal_sediment_perc = models.IntegerField(
        default=0,
        verbose_name=_('Maximal sediment')
    )

    minimal_nitrogen_perc = models.IntegerField(
        default=0,
        verbose_name=_('Minimal nitrogen')
    )

    predefined_nitrogen_perc = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Predefined nitrogen')
    )

    maximal_nitrogen_perc = models.IntegerField(
        default=0,
        verbose_name=_('Maximal nitrogen')
    )

    minimal_phoshorus_perc = models.IntegerField(
        default=0,
        verbose_name=_('Minimal phosphorus')
    )

    predefined_phosphorus_perc = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Predefined phosphorus')
    )

    maximal_phosphorus_perc = models.IntegerField(
        default=0,
        verbose_name=_('Maximal phosphorus')
    )

    minimal_transp_water_perc = models.IntegerField(
        default=0,
        verbose_name=_('Minimal transported water')
    )

    predefined_transp_water_perc = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Predefined transported water')
    )

    maximal_transp_water_perc = models.IntegerField(
        default=0,
        verbose_name=_('Maximal transported water')
    )


class DemandParameters(models.Model):

    interpolation_type = models.CharField(
        max_length=30,
        verbose_name=_('Interpolation type')
    )

    initial_extraction = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Initial extraction')
    )

    ending_extraction = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Ending extraction')
    )

    years_number = models.IntegerField(
        verbose_name=_('Years number'),
    )

    is_manual = models.BooleanField(verbose_name=_('Manual'), default=False)


class Intake(models.Model):
    """
    Model to Waterproof Intake.

    :name: Intake Name.
    :descripcion: Intake Description.

    """

    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    description = models.CharField(
        max_length=1024,
        verbose_name=_('Description'),
    )

    water_source_name = models.CharField(
        max_length=100,
        verbose_name=_('Source name'),
    )

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    demand_parameters = models.ForeignKey(DemandParameters, on_delete=models.CASCADE)

    xml_graph = models.TextField(
        verbose_name=_('Graph')
    )

    creation_date = models.DateField(auto_now=True)

    updated_date = models.DateField(auto_now=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


class Basins(models.Model):
    geom = models.PolygonField(verbose_name='geom', srid=4326, null=True, blank=True)

    continent = models.CharField(
        max_length=254,
        verbose_name=_('Continent'),
    )

    symbol = models.CharField(
        max_length=254,
        verbose_name=_('Symbol'),
    )

    code = models.IntegerField(
        default=0,
        verbose_name=_('Code')
    )

    label = models.CharField(
        max_length=50,
        verbose_name=_('Label'),
    )

    x_min = models.FloatField(
        null=False,
        blank=False,
        default=None,
        verbose_name=_('Xmin')
    )

    x_max = models.FloatField(
        null=False,
        blank=False,
        default=None,
        verbose_name=_('Xmax')
    )

    y_min = models.FloatField(
        null=False,
        blank=False,
        default=None,
        verbose_name=_('Ymin')
    )

    y_max = models.FloatField(
        null=False,
        blank=False,
        default=None,
        verbose_name=_('Ymax')
    )


class Polygon(models.Model):

    area = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('Awy')
    )

    geom = models.PolygonField(verbose_name='geom', srid=4326, null=True, blank=True)

    delimitation_date = models.DateField(auto_now=True)

    delimitation_type = models.CharField(
        max_length=30,
        verbose_name=_('Delimitation type')
    )

    basin = models.ForeignKey(Basins, on_delete=models.CASCADE)

    intake = models.ForeignKey(Intake, on_delete=models.CASCADE)


class ExternalInputs(models.Model):
    year = models.IntegerField(
        default=1980,
        verbose_name=_('Year')
    )

    water_volume = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Water_volume')
    )

    sediment = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Extraction value')
    )

    nitrogen = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Extraction value')
    )

    phosphorus = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Extraction value')
    )

    intake = models.ForeignKey(Intake, on_delete=models.CASCADE)


class ElementSystem(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    normalized_category = models.CharField(
        max_length=100,
        verbose_name=_('Normalized category')
    )

    origin = models.IntegerField(
        default=1980,
        verbose_name=_('Year'),
    )

    destination = models.IntegerField(
        default=1980,
        verbose_name=_('Year'),
    )

    sediment = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Extraction value')
    )

    nitrogen = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Extraction value')
    )

    phosphorus = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Extraction value')
    )

    intake = models.ForeignKey(Intake, on_delete=models.CASCADE)

    """
    user_cost = models.ManyToManyField(
        UserCosts,
    )

    system_cost = models.ManyToManyField(
        SystemCosts,
    )
    """

    awy = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('Awy')
    )

    q_l_s = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('Qls')
    )

    wsed_ton = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('WsedTon')
    )

    wn_kg = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('WnKg')
    )

    csed_mg_l = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('CsedMgL')
    )

    cn_mg_l = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('Cn')
    )

    cp_mg_l = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('CpMgl')
    )

    wsed_ret_ton = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('WsedRetTon')
    )

    wn_ret_kg = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('WnRetKg')
    )

    wp_ret_ton = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('WpRetTon')
    )


class WaterExtraction(models.Model):
    year = models.IntegerField(
        default=0,
        verbose_name=_('Year'),
    )

    value = models.DecimalField(
        decimal_places=4,
        max_digits=14,
        verbose_name=_('Extraction value')
    )

    demand = models.ForeignKey(DemandParameters, on_delete=models.CASCADE)
