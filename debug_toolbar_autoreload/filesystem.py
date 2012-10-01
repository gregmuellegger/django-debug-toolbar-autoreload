import os
import sys


_win = (sys.platform == "win32")

def get_mtimes(filenames):
    global _win
    _mtimes = {}
    for filename in filenames:
        if not os.path.exists(filename):
            continue
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if _win:
            mtime -= stat.st_ctime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
    return _mtimes


def get_source_files():
    def module_to_filename(module):
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

    return [
        filename
        for filename in map(module_to_filename, sys.modules.values())
        if filename]


class FileWatcher(object):
    def __init__(self, paths=None):
        self._paths = paths
        self.initial_mtimes = get_mtimes(self.get_paths())
        self.current_mtimes = self.initial_mtimes.copy()

    def get_paths(self):
        return [
            filename
            for filename in self._paths
            if os.path.exists(filename)]

    def get_updated_files(self):
        paths = self.get_paths()
        self.current_mtimes = get_mtimes(paths)
        modified = []
        for path in paths:
            # file was deleted
            if path in self.initial_mtimes and path not in self.current_mtimes:
                pass
            # file was created
            elif path not in self.initial_mtimes and path in self.current_mtimes:
                modified.append(path)
            # file was modified
            elif self.current_mtimes[path] != self.initial_mtimes[path]:
                modified.append(path)
        return modified

    def has_updates(self):
        return len(self.get_updated_files()) > 0


class SourceWatcher(FileWatcher):
    def __init__(self):
        super(SourceWatcher, self).__init__()

    def get_paths(self):
        return get_source_files()
