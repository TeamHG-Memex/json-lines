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


def reader(path_or_file, broken=False):
    """
    Read .jl or .jl.gz file with JSON lines data,
    return iterator with decoded lines.
    If the .jl.gz archive is broken as much lines as possible are read from
    the archive, and then an error is logged.
    """
    if isinstance(path_or_file, six.string_types):
        file = open_file(path_or_file, 'rb')
        needs_closing = True
    else:
        file = path_or_file
        needs_closing = False
    try:
        for line in file:
            try:
                yield json.loads(line.decode('utf8'))
            except Exception as e:
                if not broken:
                    raise
                logging.warning(
                    'Error found: JSON line can\'t be decoded. %r' % e)
                break
    except Exception:
        if not broken:
            raise
        logging.warning('Error found: truncated archive.')
    finally:
        if needs_closing:
            file.close()
