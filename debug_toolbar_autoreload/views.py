import time
from django.http import HttpResponse
from django.utils import simplejson
from .filesystem import FileWatcher, SourceWatcher
from .filesystem import Resource, MediaResource


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
    source_watcher = SourceWatcher()
    updates = None
    while not updates:
        time.sleep(0.5)
        # break the watching action and return a response to release the
        # running thread. This is necessary since the looped check would
        # prevent django from loading changed source code.
        if source_watcher.has_updates():
            response = HttpResponse()
            response.status_code = 204
            return response
        updates = file_watcher.get_updated_files()
    response = HttpResponse(simplejson.dumps([
        {'src': resource.name, 'mtime': resource.mtime}
        for resource in updates
    ]))
    return response
