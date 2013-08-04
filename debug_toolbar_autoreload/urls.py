try:
    from django.conf.urls import patterns, url
except ImportError: # django < 1.4
    from django.conf.urls.defaults import patterns, url
from debug_toolbar.urls import _PREFIX


AUTORELOAD_URL = u'/%s/autoreload/' % _PREFIX


urlpatterns = patterns('debug_toolbar_autoreload.views',
    url(r'^%s/autoreload/$' % _PREFIX, 'notify', name='djdt-autoreload'),
)
