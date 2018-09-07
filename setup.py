#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='rmtest',
    version='0.7.0',

    description='Redis Module Testing Utility',
    url='http://github.com/goodform/rmtest',
    packages=find_packages(),
    install_requires=['redis'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Testing'
    ]
)
