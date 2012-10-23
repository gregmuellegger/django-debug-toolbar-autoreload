import os
import time
from django.http import HttpResponse
from django.utils import simplejson
from . import conf
from .filesystem import FileWatcher, SourceWatcher
from .filesystem import Resource, MediaResource


class Suspender(object):
    timeout = conf.AUTORELOAD_TIMEOUT

    def __init__(self):
        self.parent_process_id = os.getppid()
        self.source_watcher = SourceWatcher()
        self.start_time = time.time()

    def should_suspend(self):
        # return after a set amount of time in case the other checks fail.
        if self.timeout:
            if time.time() - self.start_time > self.timeout:
                return True
        # if the parent process id changed (most likely to 1) means that the
        # process got daemonized. In case of django, this means that the
        # development server wants to shutdown.
        if self.parent_process_id != os.getppid():
            return True
        # We need to suspend if the source code has changed. Otherwise
        # django's autoreloader won't be able to reload the server until all
        # requests are finished.
        if self.source_watcher.has_updates():
            return True
        return False


def notify(request):
    '''
    This view gets a POST request from the Javascript part of the
    AutoreloadPanel that contains a body that looks like::

        template=/full/path/to/template.html&template=/another/template.eml:123456789&
        media=/static/url/to/a/file:133456780&media=http://media.localhost.local/base.css

    It is a list of template paths and a list of URLs that are part of the
    static/media directories of the project. The filename might be followed by
    a unix-epoch timestamp of the last modified date, seperated by a colon.

    The view then blocks the response as long until one of the specified files
    has a modified-time that is newer than the specified timestamp. It will
    return a line seperated list of those changed files.

    The view might also return with an empty response and status 204 (No
    Content) if the source code that the development server runs was modified.
    This is needed to free the current thread and allow django's runserver
    command to reload the source code, to take those changes into account.
    '''
    def get_resources(names, resource_class):
        resources = []
        for name in names:
            timestamp = None
            if ':' in name:
                name, timestamp = name.split(':', 1)
                try:
                    timestamp = float(timestamp)
                except (ValueError, TypeError):
                    timestamp = None
            resources.append(resource_class(name, timestamp))
        return resources

    resources = get_resources(request.REQUEST.getlist('template'), Resource)
    resources += get_resources(request.REQUEST.getlist('media'), MediaResource)

    file_watcher = FileWatcher(resources)
    suspender = Suspender()
    updates = None
    while not updates:
        time.sleep(0.5)
        # break the watching action and return a response to release the
        # running thread. This is necessary since the looped check would
        # prevent django from loading changed source code or quitting the
        # development server with CTRL-C
        if suspender.should_suspend():
            response = HttpResponse()
            response.status_code = 204
            return response
        updates = file_watcher.get_updated_files()
    response = HttpResponse(simplejson.dumps([
        {'src': resource.name, 'mtime': resource.mtime}
        for resource in updates
    ]))
    return response
