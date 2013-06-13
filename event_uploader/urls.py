from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',

    url(r'^upload-events/$', 
        'event_uploader.views.import_events_spreadsheet', 
        name='import_events'),
    )

