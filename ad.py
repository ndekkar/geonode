import ldap
import ldap.modlist
import geonode.settings as settings
from geonode.datarequests.models import profile_request 
from pprint import pprint

def search_dn(uname):
    con =ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
    con.set_option(ldap.OPT_REFERRALS, 0)
    con.simple_bind_s(settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD)
    result = con.search_s(settings.AUTH_LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(sAMAccountName="+uname+")", ['o','company'])
    pprint(result)
    con.unbind_s()
    for x,fields in result:
        if x:
            y = None
            if 'o' in list(fields.keys()):
                y = fields['o']
            return x,y

def add_company_organization(dn, company = None, org = None, initial_org = None):
    mod_attrs = []
    if not company and not org:
        raise Exception("Are you fucking kidding me?")
    if company:
        mod_attrs.append(
            (ldap.MOD_ADD, 'company', company)
        )
    if org:
        if not initial_org or len(initial_org) < 1:
            mod_attrs.append(
                (ldap.MOD_ADD, 'o', org)
            )
    try:
        con = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
        con.set_option(ldap.OPT_REFERRALS, 0)
        con.simple_bind_s(settings.LIPAD_LDAP_BIND_DN, settings.LIPAD_LDAP_BIND_PW)
        result = con.modify_s(dn, mod_attrs)
        con.unbind_s()
        return result
    except Exception as e:
        import traceback
        print traceback.format_exc()
        return e

def test():
    test_list = ['test_dac-group','test_dac-leaders','test_dpc-lms','test_dlms_alms',
        'test_dleaders_alms','test_dpc-terra','test_dterra-aterra','test_dleaders_aterra','test_dpc-arc']
    for t in test_list:
        dn, organization = search_dn(t)
        pprint(add_company_organization(dn,company="Other",org="test",initial_org = organization))
    
def live():
    for r in profile_request.objects.exclude(profile=None):
        uname = r.profile.username
        dn, organization = search_dn(uname)
        pprint(add_company_organization(dn,company=r.org_type,org=r.organization,initial_org = organization))
