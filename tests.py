import gzip
import json
import tempfile

import json_lines


def jl_bytes(data):
    return '\n'.join(json.dumps(x) for x in data).encode('utf8')


def test_reader_path():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        data = [{'a': 1}, {'b': 2}]
        f.write(jl_bytes(data))
        f.close()
        with json_lines.open_file(f.name) as f_:
            assert list(json_lines.reader(f_)) == data


def test_reader_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        data = [{'a': 1}, {'b': 2}]
        f.write(jl_bytes(data))
        f.close()
        with open(f.name, 'rb') as f_:
            assert list(json_lines.reader(f_)) == data


def test_reader_gzip_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.close()
        data = [{'a': 1}, {'b': 2}]
        with gzip.open(f.name, 'wb') as gzip_f:
            gzip_f.write(jl_bytes(data))
        with gzip.open(f.name, 'rb') as f_:
            assert list(json_lines.reader(f_)) == data


def test_reader_gzip_path():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jl.gz') as f:
        f.close()
        data = [{'a': 1}, {'b': 2}]
        with gzip.open(f.name, 'wb') as gzip_f:
            gzip_f.write(jl_bytes(data))
        with json_lines.open_file(f.name) as f_:
            assert list(json_lines.reader(f_)) == data


def test_reader_broken():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jl.gz') as f:
        f.close()
        data = [{'a': 1}]
        with gzip.open(f.name, 'wb') as gzip_f:
            gzip_f.write(jl_bytes(data * 1000))
        with open(f.name, 'rb') as f_:
            contents = f_.read()
        with open(f.name, 'wb') as f_:
            f_.write(contents[:-10])
        with json_lines.open_file(f.name) as f_:
            read_data = list(json_lines.reader(f_, broken=True))
            assert read_data[:900] == data * 900


def test_reader_broken_fuzz():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jl.gz') as f:
        f.close()
        data = [{'a': 1}]
        with gzip.open(f.name, 'wb') as gzip_f:
            gzip_f.write(jl_bytes(data * 1000))
        with open(f.name, 'rb') as f_:
            contents = f_.read()
        for cut in range(1, min(1000, len(contents))):
            with open(f.name, 'wb') as f_:
                f_.write(contents[:-cut])
            with json_lines.open_file(f.name) as f_:
                read_data = list(json_lines.reader(f_, broken=True))
                assert isinstance(read_data, list)
