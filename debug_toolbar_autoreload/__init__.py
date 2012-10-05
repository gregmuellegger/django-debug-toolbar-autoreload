from django.test.signals import template_rendered
from django.utils.translation import ugettext_lazy as _
from debug_toolbar.panels import DebugPanel
from . import conf
from . import urls


class AutoreloadPanel(DebugPanel):
    """
    Panel that reloads the page if a templatefile was changed.
    """
    name = 'Autoreload'
    template = 'debug_toolbar/panels/autoreload.html'
    has_content = True

    def __init__(self, *args, **kwargs):
        super(AutoreloadPanel, self).__init__(*args, **kwargs)
        self._is_active = True
        self.templates = []
        template_rendered.connect(self._store_template_info)

    def nav_title(self):
        return _('Autoreload')

    def nav_subtitle(self):
        if conf.AUTORELOAD_ENABLED:
            return _(u'enabled')
        return _(u'disabled')

    def url(self):
        return ''

    def title(self):
        return _('Autoreload')

    def _store_template_info(self, sender, template, **kwargs):
        if template.name and template.name.startswith('debug_toolbar/'):
            return  # skip templates that we are generating through the debug toolbar.
        if template.origin:
            template_path = template.origin.name
            if template_path not in self.templates:
                self.templates.append(template_path)

    def process_request(self, request):
        self.request = request
        self.request.urlconf.urlpatterns = (
            urls.urlpatterns +
            self.request.urlconf.urlpatterns
        )

        # circumvent csrf check for the autoreload watcher view
        if self.request.path == urls.AUTORELOAD_URL:
            self.request.csrf_processing_done = True

    def process_response(self, request, response):
        self.record_stats({
            'templates': self.templates,
            'AUTORELOAD_URL': urls.AUTORELOAD_URL,
            'AUTORELOAD_ENABLED': conf.AUTORELOAD_ENABLED,
            'AUTORELOAD_FILETYPES': conf.AUTORELOAD_FILETYPES,
        })
