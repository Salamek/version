#!/usr/bin/env python
import os
import re
import sys

from setuptools import setup, find_packages

version = re.compile(r'VERSION\s*=\s*\((.*?)\)')


def get_package_version() -> str:
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "version/__init__.py")) as init_f:
        for line in init_f:
            m = version.match(line.strip())
            if not m:
                continue
            return ".".join(m.groups()[0].split(", "))

classes = """
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

setup(
    name='version',
    version=get_package_version(),
    description='Simple helper python application to set version of project and create tags in git',
    long_description=open('README.md').read(),
    author='Adam Schubert',
    author_email='adam.schubert@sg1-game.net',
    url='https://github.com/Salamek/version',
    license='GPL-3.0',
    classifiers=classifiers,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'docopt',
        'pyyaml',
        'gitpython'
    ],
    test_suite="tests",
    tests_require=[],
    entry_points={
        'console_scripts': [
            'version = version.__main__:main',
        ],
    }
)
