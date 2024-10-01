#!/usr/bin/env python

from setuptools import setup, find_packages

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
    version='1.5.3',
    description='Simple helper python application to set version of project and create tags in git',
    long_description=open('README.md').read(),
    author='Adam Schubert',
    author_email='adam.schubert@sg1-game.net',
    url='https://github.com/Salamek/version',
    license='GPL-3.0',
    classifiers=classifiers,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'packaging',
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
