import os

from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Div, Column, Row, Field
from crispy_forms.bootstrap import PrependedText, InlineRadios
from model_utils import Choices

from geonode.datarequests.models import DataRequestProfile
from geonode.layers.forms import NewLayerUploadForm
from geonode.documents.models import Document
from geonode.documents.forms import DocumentCreateForm
from geonode.people.models import OrganizationType, Profile

from .models import DataRequestProfile, RequestRejectionReason

from pprint import pprint

class DataRequestProfileForm(forms.ModelForm):

    DATA_SET_CHOICES = Choices(
        ('Topographic Map', _('Topographic Map')),
        ('Forestry/Agri/Biodiversity Map',
            _('Forestry/Agri/Biodiversity Map')),
        ('Resource Prospecting/Asset Map',
            _('Resource Prospecting/Asset Map')),
        ('Flood Hazard Map', _('Flood Hazard Map')),
        #('Landslide Hazard Map', _('Landslide Hazard Map')),
        ('Thematic Disaster 3D Layer Map',
            _('Thematic Disaster 3D Layer Map')),
        ('other', _('Other, please specify:')),
    )

    class Meta:
        model = DataRequestProfile
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'organization',
            'location',
            'email',
            'contact_number',
        )

    def __init__(self, *args, **kwargs):

        super(DataRequestProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Fieldset('Requester Information',
                Div(
                    Field('captcha', css_class='form-control'),
                    css_class='form-group'
                ),
                Div(
                    Field('first_name', css_class='form-control'),
                    css_class='form-group'
                ),
                Div(
                    Field('middle_name', css_class='form-control'),
                    css_class='form-group'
                ),
                Div(
                    Field('last_name', css_class='form-control'),
                    css_class='form-group'
                ),
                Div(
                    Field('organization', css_class='form-control'),
                    css_class='form-group'
                ),
                Div(
                    Field('location', css_class='form-control'),
                    css_class='form-group'
                ),
                Div(
                    Field('email', css_class='form-control'),
                    css_class='form-group'
                ),
                Div(
                    Field('contact_number', css_class='form-control'),
                    css_class='form-group'
                )
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_emails = Profile.objects.all().values_list('email', flat=True)
        requester_email = DataRequestProfile.objects.exclude(
            request_status='rejected'
        ).values_list('email', flat=True)

        if email in user_emails:
            raise forms.ValidationError(
                'That email is already being used by a registered user.')

        if email in requester_email:
            raise forms.ValidationError(
                "A data request registration with that email already exists.")

        return email
    
    def save(self, commit=True, *args, **kwargs):
        data_request = super(
            DataRequestProfileForm, self).save(commit=False, *args, **kwargs)

        if commit:
            data_request.save()
        return data_request


class DataRequestProfileCaptchaForm(forms.Form):
    
    INTENDED_USE_CHOICES = Choices(
        ('Disaster Risk Management', _('Disaster Risk Management')),
        ('Urban/Land Subdivision Planning',
            _('Urban/Land Subdivision Planning')),
        ('Road/Infrastracture Planning', _('Road/Infrastracture Planning')),
        ('Transport/Traffic Management', _('Transport/Traffic Management')),
        ('Oil/Gas/Geothermal/Quarries/Minerals Exploration',
            _('Oil/Gas/Geothermal/Quarries/Minerals Exploration')),
        ('Biological/Agricultural/Forestry/Marine/Natural Resource Planning',
            _('Biological/Agricultural/Forestry/Marine/Natural Resource Planning')),
        ('Cellular Network Mapping', _('Cellular Network Mapping')),
        ('other', _('Other, please specify:')),
    )

    DATASET_USE_CHOICES =Choices(
        ('commercial', _('Commercial')),
        ('noncommercial', _('Non-commercial')),
    )

    LICENSE_PERIOD_CHOICES = Choices(
        ('One-time Use', _('One-time Use')),
        ('1 Year or Less', _('1 Year or Less')),
        ('other', _('Other, please specify:')),
    )

    REQUEST_LEVEL_CHOICES = Choices(
        ('institution', _('Institution')),
        ('faculty', _('Faculty')),
        ('student', _('Student')),
    )
    
    purpose = forms.ChoiceField(
        label=_('Purpose/Intended Use of Data'),
        choices=INTENDED_USE_CHOICES
    )
    purpose_other = forms.CharField(
        label=_(u'Your custom purpose for the data'),
        required=False
    )
    
    license_period = forms.ChoiceField(
        label=_('License Period'),
        choices=LICENSE_PERIOD_CHOICES
    )
    license_period_other = forms.IntegerField(
        label=_(u'Your custom license period (in years)'),
        required=False
    )
    
    intended_use_of_dataset = forms.ChoiceField(
        label = _('Intended Use of Data Set'),
        choices = DATASET_USE_CHOICES
    )

    request_level = forms.ChoiceField(
        label=_('Level of Request'),
        choices=REQUEST_LEVEL_CHOICES
    )    
    letter_file = forms.FileField(
        label=_('Formal Request Letter'),
        required = True
    )
    captcha = ReCaptchaField(attrs={'theme': 'clean'})

    def __init__(self, *args, **kwargs):
        super(DataRequestProfileCaptchaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        # self.helper.form_show_labels = False
        self.helper.layout = Layout( 
            #Div(
                #Field('project_summary', css_class='form-control'),
                #css_class='form-group'
            #),
            #Div(
                #Field('data_type_requested', css_class='form-control'),
                #css_class='form-group'
            #),
            Div(
                Field('purpose', css_class='form-control'),
                Div(
                    Field('purpose_other', css_class='form-control'),
                    css_class='col-sm-11 col-sm-offset-1'
                ),
                css_class='form-group'
            ),
            Field('letter_file'),
            Div(
                Field('license_period', css_class='form-control'),
                Div(
                    Field('license_period_other', css_class='form-control'),
                    css_class='col-sm-11 col-sm-offset-1'
                ),
                css_class='form-group'
            ),
            #Field('has_subscription'),
            Div(
                Field('intended_use_of_dataset', css_class='form-control'),
                css_class='form-group'
            ),
            Fieldset('Non-commercial',
                Div(
                    Field('organization_type', css_class='form-control'),
                    css_class='form-group'
                ),
                css_class='noncommercial-fieldset',
            ),
            Fieldset('Academe',
                Div(
                    Field('request_level', css_class='form-control'),
                    css_class='form-group'
                ),
                Div(
                    Field('funding_source', css_class='form-control'),
                    css_class='form-group'
                ),
                Field('is_consultant'),
                css_class='academe-fieldset',
            ),
            HTML("""
                {% load i18n %}
                <section id="drop-zone">
                    <h3><i class="fa fa-cloud-upload"></i><br />{% trans "Drop files here" %}</h3>
                </section>

                <p>{% trans " or select them one by one:" %}</p>

                <input class="btn" id="file-input" type="file" multiple>
    
                <a href="#" id="clear-button" class="btn btn-danger">{% trans "Clear Files" %}</a>
                <br />
                <br />
                <section class="charset">
                <p>{% trans "Select the charset or leave default" %}</p>
                <select id="charset">
                {% for charset in charsets %}
                    {% if charset.0 == 'UTF-8' %}
                        <option selected='selected' value={{ charset.0 }}>{{ charset.1 }}</option>
                    {% else %}
                        <option value={{ charset.0 }}>{{ charset.1 }}</option>
                    {% endif %}
                {% endfor %}
                </select>
                </section>
            """),
            Div(
                HTML("<section class=widget>"),
                Field('captcha'),
                HTML("</section>")
            ),
        )

    def clean_purpose_other(self):
        purpose = self.cleaned_data.get('purpose')
        purpose_other = self.cleaned_data.get('purpose_other')
        if purpose == self.INTENDED_USE_CHOICES.other:
            if not purpose_other:
                raise forms.ValidationError(
                    'Please state your purpose for the requested data.')
        return purpose_other

    def clean_purpose(self):
        purpose = self.cleaned_data.get('purpose')
        if purpose == self.INTENDED_USE_CHOICES.other:
            purpose_other = self.cleaned_data.get('purpose_other')
            if not purpose_other:
                return purpose
            else:
                return purpose_other
        return purpose

    
    def clean_license_period_other(self):
        license_period = self.cleaned_data.get('license_period')
        license_period_other = self.cleaned_data.get('license_period_other')
        if license_period == self.LICENSE_PERIOD_CHOICES.other:
            if not license_period_other:
                raise forms.ValidationError(
                    'Please input the license period.')
        return license_period_other

    def clean_license_period(self):
        license_period = self.cleaned_data.get('license_period')
        if license_period == self.LICENSE_PERIOD_CHOICES.other:
            license_period_other = self.cleaned_data.get('license_period_other')
            if not license_period_other:
                return license_period
            else:
                return license_period_other
        return license_period
    

    def clean_funding_source(self):
        funding_source = self.cleaned_data.get('funding_source')
        organization_type = self.cleaned_data.get('organization_type')
        intended_use_of_dataset = self.cleaned_data.get('intended_use_of_dataset')
        if (intended_use_of_dataset == 'noncommercial' and
                organization_type == OrganizationType.ACADEME and
                not funding_source):
            raise forms.ValidationError(
                'This field is required.')
        return funding_source

    def clean_letter_file(self):
        letter_file = self.cleaned_data.get('letter_file')
        split_filename =  os.path.splitext(str(letter_file.name))
        
        if letter_file and split_filename[len(split_filename)-1].lower()[1:] != "pdf":
            raise forms.ValidationError(_("This file type is not allowed"))
        return letter_file

class DataRequestProfileShapefileForm(NewLayerUploadForm):
    captcha = ReCaptchaField(attrs={'theme': 'clean'})
    #project_summary = forms.CharField(widget=forms.Textarea)
    purpose = forms.ChoiceField(
        choices = DataRequestProfileCaptchaForm.INTENDED_USE_CHOICES,
        required = True
    )
    purpose_other = forms.CharField(
        required = False
    )
    

    class Meta:
        fields = (
            #'project_summary',
            'purpose',
            'purpose_other',
            'captcha',
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(DataRequestProfileShapefileForm, self).__init__(*args, **kwargs)

        self.fields['captcha'].error_messages = {'required': 'Please answer the Captcha to continue.'}

class DataRequestProfileRejectForm(forms.ModelForm):

    REJECTION_REASON_CHOICES = Choices(
        ('Invalid requirements', _('Invalid requirements')),
        ('Invalid purpose', _('Invalid purpose')),
    )

    rejection_reason = forms.ChoiceField(
        label=_('Reason for Rejection'),
        choices=REJECTION_REASON_CHOICES
    )

    class Meta:
        model = DataRequestProfile
        fields = (
            'rejection_reason', 'additional_rejection_reason',
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(DataRequestProfileRejectForm, self).__init__(*args, **kwargs)
        rejection_reason_qs = RequestRejectionReason.objects.all()
        if rejection_reason_qs:
            self.fields['rejection_reason'].choices = [(r.reason, r.reason) for r in rejection_reason_qs]
