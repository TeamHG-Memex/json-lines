import gzip


__all__ = ['maybe_gzip_open', 'path_to_str']


def maybe_gzip_open(path, *args, **kwargs):
    """
    Open file with either open or gzip.open, depending on file extension.

    This function doesn't handle json lines format, just opens a file
    in a way it is decoded transparently if needed.
    """
    path = path_to_str(path)
    if path.endswith('.gz') or path.endswith('.gzip'):
        _open = gzip.open
    else:
        _open = open
    return _open(path, *args, **kwargs)


def path_to_str(path):
    """ Convert pathlib.Path objects to str; return other objects as-is. """
    try:
        from pathlib import Path as _Path
    except ImportError:  # Python < 3.4
        class _Path:
            pass
    if isinstance(path, _Path):
        return str(path)
    return path
