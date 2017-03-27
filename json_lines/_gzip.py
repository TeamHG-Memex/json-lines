# -*- coding: utf-8 -*-
import io
import gzip
import mmap
from contextlib import closing

GZIP_SIGNATURE = b'\x1f\x8b\x08'


def get_known_read_position(fp, buffered=True):
    """ 
    Return a position in a file which is known to be read & handled.
    It assumes a buffered file and streaming processing. 
    """
    buffer_size = io.DEFAULT_BUFFER_SIZE if buffered else 0
    return max(fp.tell() - buffer_size, 0)


def recover(gzfile, last_good_position):
    # type: (gzip.GzipFile, int) -> gzip.GzipFile
    """ 
    Skip to the next possibly decompressable part of a gzip file.
    Return a new GzipFile object if such part is found or None
    if it is not found.
    """
    pos = get_recover_position(gzfile, last_good_position=last_good_position)
    if pos == -1:
        return None
    fp = gzfile.fileobj
    fp.seek(pos)
#     gzfile.close()
    return gzip.GzipFile(fileobj=fp, mode='r')


def get_recover_position(gzfile, last_good_position):
    # type: (gzip.GzipFile, int) -> int
    """
    Return position of a next gzip stream in a GzipFile, 
    or -1 if it is not found.
    
    XXX: caller must ensure that the same last_good_position
    is not used multiple times for the same gzfile.
    """
    with closing(mmap.mmap(gzfile.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        return m.find(GZIP_SIGNATURE, last_good_position + 1)
