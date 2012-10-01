import os
import time
from django.http import HttpResponse
from .filesystem import resolve_media_url, FileWatcher, SourceWatcher


def notify(request):
    resources = request.REQUEST.getlist('template')
    media_resources = request.REQUEST.getlist('media')
    media_resources = map(resolve_media_url, media_resources)
    resources = set(
        resource
        for resource in resources + media_resources
        if resource and os.path.exists(resource))

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
    response = HttpResponse('\n'.join(updates))
    return response
