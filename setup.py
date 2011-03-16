from setuptools import setup, find_packages

from pycri import __version__

setup(
    name='pycri',
    version=__version__,
    description='IRC-bot',
    author='Marcus Carlsson',
    author_email='carlsson.marcus@gmail.com',
    url='https://github.com/xintron/pycri',
    package_data={'':['*.py']},
    packages=find_packages(),
    provides=[
        'pycri',
    ],
    install_requires=['twisted'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ]
)
