import gzip
import json
import logging

import six


def open_file(path, *args, **kwargs):
    """
    Open file with either open or gzip.open, depending on file extension.
    """
    if path.endswith('.gz') or path.endswith('.gzip'):
        _open = gzip.open
    else:
        _open = open
    return _open(path, *args, **kwargs)


def reader(file, broken=False):
    """
    Read .jl or .jl.gz file with JSON lines data,
    return iterator with decoded lines.
    If the .jl.gz archive is broken as much lines as possible are read from
    the archive, and then an error is logged.
    """
    try:
        for line in file:
            try:
                if not isinstance(line, six.text_type):
                    line = line.decode('utf8')
                yield json.loads(line)
            except Exception as e:
                if not broken:
                    raise
                logging.warning(
                    'Error found: JSON line can\'t be decoded. %r' % e)
                break
    except Exception as e:
        if not broken:
            raise
        logging.warning('Error found: truncated archive. %r' % e)
