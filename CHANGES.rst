Changelog
=========

0.2.0
-----

* Don't reload the whole page if only a css file was changed. Instead load CSS
  in place.
* Adding CHANGES.rst to MANIFEST.in which caused errors during install.

0.1.1
-----

* Try to detect if development server wants to shutdown. Before this change
  was the server still running in the background and didn't allow you to
  restart it again.

0.1.0
-----

* Initial release.
