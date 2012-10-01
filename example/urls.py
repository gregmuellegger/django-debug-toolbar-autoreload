from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),
    url(r'^simple/$', direct_to_template, {'template': 'simple.html'}, name='simple'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
