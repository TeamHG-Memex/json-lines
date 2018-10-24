Release notes
=============

.. contents::

0.4.0 (2018.10.24)
------------------

- Backwards incompatible: ``json_lines.open_file`` is made private and
  renamed to ``json_lines.lib._maybe_gzip_open``;
- ``json_lines.open`` now supports pathlib.Path objects;
- docstrings are added to more functions;
- logging now uses "json_lines" logger;
- logging no longer uses string formatting;
- Python 3.7 support.


0.3.1 (2017.03.28)
------------------

- README fixed


0.3.0 (2017.03.27)
------------------

- Resume reading after error for plain and compressed files (#2)


0.2.0 (2016.09.06)
------------------

- ``json_lines.open`` added, ``open_file`` removed from docs


0.1.1 (2016.08.19)
------------------

Initial release
