#!/usr/bin/env python
import sys

from setuptools import setup, find_packages

import philip


requires = ['requests==2.7.0',
            'PyYAML==3.11',
            'docutils>=0.10',
            'argcomplete']


if sys.version_info[:2] == (2, 6):
    # For python2.6 we have to require argparse since it
    # was not in stdlib until 2.7.
    requires.append('argparse>=1.1')


setup_options = dict(
    name='philip',
    version=philip.__version__,
    description='Command Line tool for Marathon.',
    long_description=open('README.md').read(),
    author='leonmax',
    url='https://github.com/greencase/philip',
    scripts=['bin/phi'],
    packages=find_packages(exclude=['tests*']),
    package_data={'philip': ['example/*.json', 'examples/*/*.rst',
                             'config/*.yml', 'config/*.yaml', 'config/*.json']},
    install_requires=requires,
    extras_require={
        ':python_version=="2.6"': [
            'argparse>=1.1',
        ]
    },
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ),
)

setup_options['console'] = ['bin/phi']

setup(**setup_options)
hi
