#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test with:
    python setup.py build_ext --inplace
"""
DESCRIPTION = ("Complete Striped Smith-Waterman Library for Python")
LONG_DESCRIPTION = """
**ssw-py** is a Python package
Cythonized wrapped version of:

https://github.com/mengyao/Complete-Striped-Smith-Waterman-Library

Original C library authors and paper should be cited if used.

License is MIT
"""

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from Cython.Build import cythonize
import numpy.distutils.misc_util
import os
import sys
import shutil
import re
import ast

pjoin = os.path.join
rpath = os.path.relpath

PACKAGE_PATH =      os.path.abspath(os.path.dirname(__file__))
MODULE_PATH =       pjoin(PACKAGE_PATH, 'ssw')
DATASETS_PATH =     pjoin(MODULE_PATH, 'datasets')

common_include = ['lib/CSSWL/src', 'lib']

if sys.platform == 'win32':
    extra_compile_args = ['']
else:
    extra_compile_args = ['-Wno-unused-function']

# fasta dataset files to include in installation
ssw_files = [rpath(pjoin(root, f), MODULE_PATH) for root, _, files in
                 os.walk(DATASETS_PATH) for f in files if '.fa' in f]

ssw_ext = Extension(
    'ssw.sswpy',
    depends=[],
    sources=['ssw/sswpy.pyx',
             'lib/CSSWL/src/ssw.c',
             'lib/str_util.c'],
    include_dirs=common_include + [numpy.get_include()],
    extra_compile_args=extra_compile_args
)
# ssw_files.append('sswpy.pxd')

is_py_3 = int(sys.version_info[0] > 2)

cython_extensions = [
    ssw_ext
]
cython_ext_list = cythonize(cython_extensions,
                            compile_time_env={'IS_PY_THREE': is_py_3})

# Initialize subtree with
# git subtree add --prefix=lib/CSSWL git@github.com:mengyao/Complete-Striped-Smith-Waterman-Library.git master

# Begin modified code from Flask's version getter
# BSD license
# Copyright (c) 2015 by Armin Ronacher and contributors.
# https://github.com/pallets/flask
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('ssw/__init__.py', 'rb') as initfile:
    VERSION = str(ast.literal_eval(_version_re.search(
                                   initfile.read().decode('utf-8')).group(1)))

DISTNAME = 'ssw-py'
LICENSE = 'MIT'
AUTHORS = "Nick Conway"
EMAIL = "nick.conway@wyss.harvard.edu"
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Cython',
    'Topic :: Scientific/Engineering',
]

setup(
    name=DISTNAME,
    version=VERSION,
    author=AUTHORS,
    author_email=EMAIL,
    url='https://github.com/Wyss/ssw-py',
    packages=['ssw'],
    ext_modules=cython_ext_list,
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
    package_data={'ssw': ssw_files},
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    zip_safe=False
)