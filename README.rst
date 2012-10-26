django-debug-toolbar-autoreload
===============================

This package contains an extra panel for the excellent django-debug-toolbar_.

The purpose is to automatically reload the page if a template that was used to
render the current page is changed. It is for your browser what the
``runserver``'s auto-reload feature is for your python code.

Watch this screencast for a short introduction: http://www.youtube.com/watch?v=zQSoJF70if4

.. _django-debug-toolbar: http://pypi.python.org/pypi/django-debug-toolbar

Install
-------

1. Put the ``debug_toolbar_autoreload`` source folder in your ``PYTHONPATH``.
2. Add ``'debug_toolbar_autoreload'`` to your ``INSTALLED_APPS`` settings.
3. Add ``'debug_toolbar_autoreload.AutoreloadPanel'`` to your ``DEBUG_TOOLBAR_PANELS``.

This means your settings file should look something like::

    INSTALLED_APPS = (
        # ... other apps ...
        'debug_toolbar',
        'debug_toolbar_autoreload',
    )

    DEBUG_TOOLBAR_PANELS = (
        # default panels
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.profiling.ProfilingDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.cache.CacheDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',

        # autoreload panel
        'debug_toolbar_autoreload.AutoreloadPanel',
    )

**Requirements:** Django 1.4 or higher is required since we need a
multithreaded development server.

Contribute
----------

1. Download and setup the project::

    git clone https://github.com/gregmuellegger/django-debug-toolbar-autoreload.git
    cd django-debug-toolbar-autoreload
    virtualenv .
    source bin/activate
    pip install -r requirements/development.txt
    python manage.py syncdb
    python manage.py runserver

2. Open one of the demo pages from http://localhost:8000/ in your browser.
3. Hack
4. Send a pull request
