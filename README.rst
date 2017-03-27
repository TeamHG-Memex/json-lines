json-lines
==========

.. image:: https://img.shields.io/pypi/v/json-lines.svg
   :target: https://pypi.python.org/pypi/json-lines
   :alt: PyPI Version

.. image:: https://travis-ci.org/TeamHG-Memex/json-lines.svg?branch=master
   :target: http://travis-ci.org/TeamHG-Memex/json-lines
   :alt: Build Status

.. image:: http://codecov.io/github/TeamHG-Memex/json-lines/coverage.svg?branch=master
   :target: http://codecov.io/github/TeamHG-Memex/json-lines?branch=master
   :alt: Code Coverage

This is a tiny library for reading JSON lines (.jl) files,
including gzipped and broken files.

`JSON lines <http://jsonlines.org/>`_ is a text file format
where each line is a single json encoded item.


Why?
----

Reading a well-formed JSON lines file is a one-liner in Python.
But if the file can be broken (this happens when the process writing
it is killed), handling all exceptions takes 10x more code, especially
when the file is compressed. If file is concatenated from multiple
broken archives (some process was writing to the same file multiple times),
things get even more complicated.

json-lines handles all this cases for you!


Installation
------------

::

    pip install json-lines

If `ujson <https://pypi.python.org/pypi/ujson>`_ is installed, it is used
to speed up json decoding (which is the main performance bottleneck
even for gzipped files).


Usage
-----

In order to read a well-formed json lined file,
pass an open file as the first argument to ``json_lines.reader``.
The file can be opened
in text or binary mode, but if it's opened in text mode, the encoding
must be set correctly::

    import json_lines

    with open('file.jl', 'rb') as f:
        for item in json_lines.reader(f):
            print(item['x'])

There is also a helper function ``json_lines.open`` that recognizes
".gz" and ".gzip" extensions and opens them with ``gzip``::

    with json_lines.open('file.jl.gz') as f:
        for item in f:
            print(item['x'])

Handling broken (cut at some point) files is enabled by passing ``broken=True``
to ``json_lines.reader`` or ``json_lines.open``.
They are read while it's possible to decode the compressed stream and parse json,
silently stopping on the first json parse error (only logging a warning).
Multiple concatenated broken archives are also supported, the reader will try
to skip to the next valid gzip start::

    with json_lines.open('file.jl.gz', broken=True) as f:
        for item in f:
            print(item['x'])


License
-------

License is MIT.
