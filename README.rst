json-lines
==========

This is a tiny library for reading JSON lines (.jl) files,
including gzipped and broken files.

`JSON lines <http://jsonlines.org/>`_ is a text file format
where each line is a single json encoded item.


Why?
----

Reading a well-formed JSON lines file is a one-liner in Python.
But if the file can be broken (this happens when the process writing
it is killed), handling all exceptions takes 10x more code, especially
when the file is compressed.


Installation
------------

::

    pip install json-lines


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

There is also a helper function ``json_lines.open_file`` that recognizes
".gz" and ".gzip" extensions and opens them with ``gzip``::

    with json_lines.open_file('file.jl.gz') as f:
        for item in json_lines.reader(f):
            print(item['x'])

Handling broken (cut at some point) files is enabled by passing ``broken=True``
to ``json_lines.reader``. They are read while it's possible
to decode the compressed stream and parse json,
silently stopping on the first error (only logging a warning)::

    with json_lines.open_file('file.jl.gz') as f:
        for item in json_lines.reader(f, broken=True):
            print(item['x'])


License
-------

License is MIT.
