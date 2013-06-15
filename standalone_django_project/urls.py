from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    url('^$', 'standalone_django_project.views.home', name='home'),
    url('', include('event_uploader.urls')),

    url(r'^admin/actionkit/test_connection/', 'standalone_django_project.views.actionkit_test_connection'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

urlpatterns += patterns(
    'django.contrib.auth.views',
    (r'^accounts/login/$', 'login'),
    (r'^accounts/logout/$', 'logout'),
    )
