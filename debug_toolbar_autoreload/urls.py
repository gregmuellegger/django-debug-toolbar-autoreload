from django.conf.urls.defaults import *
from debug_toolbar.urls import _PREFIX


AUTORELOAD_URL = u'/%s/autoreload/' % _PREFIX


urlpatterns = patterns('debug_toolbar_autoreload.views',
    url(r'^%s/autoreload/$' % _PREFIX, 'notify', name='djdt-autoreload'),
)
