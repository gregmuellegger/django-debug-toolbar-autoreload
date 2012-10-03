import time
from django.http import HttpResponse
from .filesystem import FileWatcher, SourceWatcher
from .filesystem import Resource, MediaResource


def notify(request):
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
    response = HttpResponse('\n'.join(
        '%s:%s' % (resource.name, resource.mtime)
        for resource in updates
    ))
    return response
