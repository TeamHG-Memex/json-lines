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
pass a path or an open (in binary mode) file as the first argument::

    import json_lines

    for item in json_lines.reader('file.jl'):
        print(item['x'])

Reading files in gzip format (".gz" and ".gzip" extensions recognized)::

    json_lines.reader('file.jl.gz')

Handling broken (cut at some point) files: read while it's possible
to decode the compressed stream and parse json,
silently stopping on the first error (only logging a warning)::

    json_lines.reader('file.jl.gz', broken=True)

If you pass a file path as the first argument, the file is closed only if
all items are read.

You can pass an open file (it must be opened in binary mode)
as the first argument too::

    with gzip.open('file.jl.gz', 'rb') as f:
        for item in json_lines.reader(f):
            break


License
-------

License is MIT.
