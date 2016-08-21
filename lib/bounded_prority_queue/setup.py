#!/usr/bin/env python
import sys
from setuptools import setup


PYTHON3K = sys.version_info[0] > 2

setup(
    name="bounded_priority_queue",
    version='1.0',
    packages=['bounded_priority_queue'],
    zip_safe=False,
    author="Test",
    author_email="test@gmail.com",
    url="http://test.com",
    description="A bounded priority queue, used for Kd-Tree implementation.",
    long_description="A bounded priority queue, used for Kd-Tree implementation.",
    license="ASL",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    tests_require=['mock'] + [] if PYTHON3K else ['unittest2'],
    test_suite="tests" if PYTHON3K else "unittest2.collector"
)
