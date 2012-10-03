import os
import posixpath
import sys
import time
from django.conf import settings
from django.contrib.staticfiles import finders


_win = (sys.platform == "win32")


def get_mtime(filename):
    stat = os.stat(filename)
    mtime = stat.st_mtime
    if _win:
        mtime -= stat.st_ctime
    return mtime


def resolve_media_url(url):
    if settings.MEDIA_URL and url.startswith(settings.MEDIA_URL):
        filename = url[len(settings.MEDIA_URL):]
        filename = posixpath.normpath(filename).lstrip('/')
        filename = os.path.join(settings.MEDIA_ROOT, filename)
        return filename
    if settings.STATIC_URL and url.startswith(settings.STATIC_URL):
        filename = url[len(settings.STATIC_URL):]
        filename = posixpath.normpath(filename).lstrip('/')
        filename = finders.find(filename)
        return filename


class FileWatcher(object):
    def __init__(self, resources):
        self._resources = resources

    @property
    def resources(self):
        return self._resources

    def get_updated_files(self):
        modified = []
        for resource in self.resources:
            if resource.modified():
                modified.append(resource)
        return modified

    def has_updates(self):
        for resource in self.resources:
            if resource.modified():
                return True
        return False


class SourceWatcher(FileWatcher):
    def __init__(self):
        self._timestamp = time.time()

    def _module_to_filename(self, module):
        filename = getattr(module, '__file__', None)
        if filename is None:
            return filename
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if filename.endswith("$py.class"):
            filename = filename[:-9] + ".py"
        if not os.path.exists(filename):
            return None
        return filename

    def get_source_files(self):
        return [
            filename
            for filename in map(
                self._module_to_filename,
                sys.modules.values())
            if filename]

    @property
    def resources(self):
        sources = self.get_source_files()
        sources = [Resource(src, self._timestamp) for src in sources]
        return sources


class Resource(object):
    def __init__(self, name, timestamp=None):
        self.name = name
        self.timestamp = timestamp or time.time()
        self._exists = self.exists()

    @property
    def path(self):
        return self.name

    def exists(self):
        return os.path.exists(self.path)

    def modified(self):
        # delete was created or deleted
        if self._exists != self.exists():
            return True
        mtime = get_mtime(self.path)
        if mtime > self.timestamp:
            return True
        return False

    @property
    def mtime(self):
        if self.exists():
            return get_mtime(self.path)

    def __unicode__(self):
        return self.name
    __str__ = __unicode__


class MediaResource(Resource):
    @property
    def path(self):
        return resolve_media_url(self.name)
