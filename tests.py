import gzip
import json
import random

import pytest

import json_lines


def write_gz(path, data, mode='wb'):
    with gzip.open(str(path), mode) as f:
        f.write(data)


def write_jl_gz(path, data, mode='wb'):
    write_gz(path, data=jl_bytes(data), mode=mode)


def jl_bytes(data):
    return '\n'.join(json.dumps(x) for x in data).encode('utf8')


def test_reader_path(tmpdir):
    data = [{'a': 1}, {'b': 2}]
    p = tmpdir.join('myfile.jl')
    p.write_binary(jl_bytes(data))

    with json_lines.open_file(str(p)) as f:
        assert list(json_lines.reader(f)) == data


def test_reader_file(tmpdir):
    data = [{'a': 1}, {'b': 2}]
    p = tmpdir.join('myfile.jl')
    p.write_binary(jl_bytes(data))

    with open(str(p), 'rb') as f:
        assert list(json_lines.reader(f)) == data


def test_reader_gzip_file(tmpdir):
    data = [{'a': 1}, {'b': 2}]
    p = tmpdir.join('myfile.jl')
    write_jl_gz(p, data)

    with gzip.open(str(p), 'rb') as f:
        assert list(json_lines.reader(f)) == data


def test_reader_gzip_path(tmpdir):
    data = [{'a': 1}, {'b': 2}]
    p = tmpdir.join('myfile.jl.gz')
    write_jl_gz(p, data)

    with json_lines.open_file(str(p)) as f_:
        assert list(json_lines.reader(f_)) == data


def test_reader_broken_fail(tmpdir):
    p = tmpdir.join('myfile.jl.gz')
    p.write_binary(b'somedata')

    with json_lines.open_file(str(p)) as f_:
        with pytest.raises(Exception):
            _ = list(json_lines.reader(f_))


def test_reader_broken_json_fail(tmpdir):
    p = tmpdir.join('myfile.jl.gz')
    write_gz(p, b'{"a": 1}\n{[]')

    with json_lines.open_file(str(p)) as f_:
        with pytest.raises(Exception):
            _ = list(json_lines.reader(f_))


def test_reader_broken_single(tmpdir):
    p = tmpdir.join('myfile.jl.gz')
    data = [{'a': 1}]
    write_jl_gz(p, data * 1000)
    p.write_binary(p.read_binary()[:-10])

    with json_lines.open_file(str(p)) as f_:
        read_data = list(json_lines.reader(f_, broken=True))
        assert read_data[:900] == data * 900


def test_reader_broken_multiple(tmpdir):
    p = tmpdir.join('myfile.jl.gz')
    data_a = [{'a': random.random()} for _ in range(1000)]
    data_b = [{'b': random.random()} for _ in range(1000)]

    write_jl_gz(p, data_a)
    p.write_binary(p.read_binary()[:-10])
    write_jl_gz(p, data_b, 'ab')

    with json_lines.open_file(str(p)) as f:
        read_data = list(json_lines.reader(f, broken=True))
        assert read_data[:900] == data_a[:900]  # first part is recovered
        assert read_data[-1000:] == data_b  # second part is recovered


def test_reader_broken_json(tmpdir):
    p = tmpdir.join('myfile.jl.gz')
    write_gz(p, b'{"a": 1}\n{[]')

    with json_lines.open_file(str(p)) as f_:
        read_data = list(json_lines.reader(f_, broken=True))
        assert read_data == [{'a': 1}]


def test_reader_broken_json_partial(tmpdir):
    # with broken=True broken json lines are skipped, but reading continues
    p = tmpdir.join('myfile.jl')
    p.write_binary(b'{"a": 1}\n{"a": 2\n{"b": 1}\n')
    with json_lines.open(str(p), broken=True) as f:
        lines = list(f)
    assert lines == [{'a': 1}, {'b': 1}]


def test_reader_broken_json_partial_gzipped(tmpdir):
    # For gzip files broken=True only means gzip recovery, inside a single
    # archive processing stops at first broken json line
    p = tmpdir.join('myfile.jl.gz')
    write_gz(p, b'{"a": 1}\n{"a": 2\n{"b": 1}\n')
    with json_lines.open(str(p), broken=True) as f:
        lines = list(f)
    assert lines == [{'a': 1}]


def test_reader_broken_fuzz(tmpdir):
    p = tmpdir.join('myfile.jl.gz')
    data = [{'a': 1}]
    write_jl_gz(p, data * 1000)
    contents = p.read_binary()

    for cut in range(1, min(1000, len(contents))):
        p.write_binary(contents[:-cut])
        with json_lines.open_file(str(p)) as f_:
            read_data = list(json_lines.reader(f_, broken=True))
            assert isinstance(read_data, list)
