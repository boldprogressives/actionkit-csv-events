from djangohelpers.lib import allow_http, rendered_with

@allow_http("GET")
@rendered_with("standalone_django_project/home.html")
def home(request):
    return {}
