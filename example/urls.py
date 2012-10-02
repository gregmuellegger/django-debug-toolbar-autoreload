from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),
    url(r'^simple/$', direct_to_template, {'template': 'simple.html'}, name='simple'),
    url(r'^css/$', direct_to_template, {'template': 'css.html'}, name='css'),
    url(r'^full/$', direct_to_template, {'template': 'full.html'}, name='full'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
