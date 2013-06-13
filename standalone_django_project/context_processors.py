from django.conf import settings

def globals(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        }
