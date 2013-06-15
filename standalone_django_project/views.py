from actionkit import Client as get_client
from django.conf import settings
from actionkit.models import CoreUser
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from djangohelpers.lib import allow_http, rendered_with
import MySQLdb
import socket
import xmlrpclib

@allow_http("GET")
@rendered_with("standalone_django_project/home.html")
def home(request):
    return {}

@user_passes_test(lambda u: u.is_superuser)
@allow_http("GET")
def actionkit_test_connection(request):
    ak = get_client()
    try:
        version = ak.version()
    except socket.gaierror, e:
        if e.errno == 8:
            return HttpResponse(_("Could not connect to ACTIONKIT_API_HOST \"%(host)s\"; perhaps it is misspelled?  Please double check your configuration.") % {'host': settings.ACTIONKIT_API_HOST})
        else:
            raise
    except xmlrpclib.ProtocolError, e:
        if e.errcode == 401:
            return HttpResponse(_("Could not log in to Actionkit API with username \"%(username)s\" and password \"%(password)s\".  Please double check your configuration.") % {'username': settings.ACTIONKIT_API_USER, 'password': settings.ACTIONKIT_API_PASSWORD})
        else:
            raise
    except xmlrpclib.Fault, e:
        if e.faultCode == 'NotAuthorized':
            return HttpResponse(_("The Actionkit API user \"%(username)s\" does not have the required permissions.  The API user will need Superuser (but not Staff) status.  Please double check the user's permissions in the Actionkit Admin.  Log into Actionkit, select the Users tab, and select \"Add staff user.\"") % {'username': settings.ACTIONKIT_API_USER})
        else:
            raise

    try:
        user = CoreUser.objects.using("ak").get(id=1)
    except MySQLdb.OperationalError, e:
        if e.args[0] == 1045:
            return HttpResponse(_("Could not connect to the Actionkit datatabase -- please double check your ACTIONKIT_DATABASE_USER (\"%(user)s\"), ACTIONKIT_DATABASE_PASSWORD and ACTIONKIT_DATABASE_NAME (\"%(name)s\") settings.") % {'user': settings.ACTIONKIT_DATABASE_USER, 'name': settings.ACTIONKIT_DATABASE_NAME})
        else:
            raise

    return HttpResponse(_("Everything's looking good! %(msg)s") % {'msg': version})
