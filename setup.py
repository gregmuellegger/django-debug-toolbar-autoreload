# -*- coding: utf-8 -*-
import codecs
import re
import os
from distutils.core import setup
from setuptools import find_packages


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = '\n\n'.join((
    read('README.rst'),
    read('CHANGES.rst'),
))


setup(
    name='django-debug-toolbar-autoreload',
    version=find_version('debug_toolbar_autoreload', '__init__.py'),
    author=u'Gregor Müllegger',
    author_email='gregor@muellegger.de',
    packages=find_packages(exclude=('example',)),
    include_package_data=True,
    url='https://github.com/gregmuellegger/django-debug-toolbar-autoreload',
    license='BSD licence, see LICENSE file',
    description='Automatically reloads your browser when a template, css or javascript file was modified.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
