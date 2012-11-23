"""
pycri
=====

Modular IRC-bot with support for live reloading of plugins. Support for
SSL-connections.
"""
from setuptools import setup

from pycri import __version__ as version

setup(
    name='pycri',
    version=version,
    description='IRC-bot',
    long_description=__doc__,
    author='Marcus Carlsson',
    author_email='carlsson.marcus@gmail.com',
    url='https://github.com/xintron/pycri',
    packages=['pycri', 'pycri.plugins', 'pycri.utils'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    provides=[
        'pycri',
    ],
    install_requires=['twisted'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ]
)
