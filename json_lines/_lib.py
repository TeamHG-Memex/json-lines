from __future__ import absolute_import
from contextlib import contextmanager
try:
    import ujson as json
except ImportError:
    import json
import json
import logging
import six

from .utils import maybe_gzip_open
from ._gzip import recover, get_known_read_position


__all__ = ['open', 'reader']


logger = logging.getLogger("json_lines")


@contextmanager
def open(path, broken=False):
    """
    Context manager for opening and reading json lines files.
    If file extension suggests gzip (.gz or .gzip), file is
    decompressed on fly.

    Pass broken=True if you expect the file can be truncated
    or broken otherwise; reader will try to recover as much data
    as possible in this case.
    """
    with maybe_gzip_open(path) as f:
        yield reader(f, broken=broken)


def reader(file, broken=False):
    """
    Read .jl or .jl.gz file with JSON lines data,
    return iterator with decoded lines.
    If the .jl.gz archive is broken as much lines as possible are read from
    the archive.
    """
    if not broken:
        return _iter_json_lines(file)
    else:
        return _iter_json_lines_recovering(file)


def _iter_json_lines(file):
    return (_decode_json_line(line) for line in file)


def _decode_json_line(line):
    if not isinstance(line, six.text_type):
        line = line.decode('utf8')
    return json.loads(line)


def _iter_json_lines_recovering(file):
    is_gzip = hasattr(file, 'fileobj')
    jl_reader = _JlRecoveringReader(file,
                                    recover_gzip=is_gzip,
                                    recover_jl=not is_gzip)
    while True:
        try:
            for line in jl_reader.iter_lines():
                yield line
            return
        except Exception as e:
            logger.warning("Error found, trying to recover from %r", e)
            if not jl_reader.try_gzip_recovering():
                logging.warning("Can't recover.")
                return
            logger.warning('Recovery successful, starting again from %s',
                           jl_reader.last_good_position)


class _JlRecoveringReader(object):
    def __init__(self, file, recover_gzip=True, recover_jl=False):
        self.last_good_position = 0
        self.file = file
        self.recover_jl = recover_jl
        self.recover_gzip = recover_gzip

    def iter_lines(self):
        for line in self.file:
            try:
                yield _decode_json_line(line)
            except Exception as e:
                if not self.recover_jl:
                    raise
                logger.warning("Error: JSON line can't be decoded. %r", e)
            else:
                if self.recover_gzip:
                    self._mark_good(self.file, buffered=True)

    def try_gzip_recovering(self):
        if not self.recover_gzip:
            return False

        logger.debug(
            "Position: %s current, %s certainly handled, %s last good",
            self.file.fileobj.tell(),
            get_known_read_position(self.file.fileobj),
            self.last_good_position,
        )
        self.file = recover(self.file,
                            last_good_position=self.last_good_position)
        if self.file is None:
            return False
        self._mark_good(self.file, buffered=False)
        return True

    def _mark_good(self, file, buffered):
        self.last_good_position = get_known_read_position(file.fileobj,
                                                          buffered)
