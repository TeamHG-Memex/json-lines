import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='json-lines',
    version='0.4.0',
    description='Reading JSON lines (jl) files, recover broken files',
    license='MIT',
    url='https://github.com/TeamHG-Memex/json-lines',
    packages=['json_lines'],
    long_description=read('README.rst'),
    install_requires=[
        'six',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
