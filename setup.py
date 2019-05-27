from setuptools import setup, find_packages
from os import path
from odt2md import (
    __version__,
    __description__,
    __keywords__,
    __url__,
    __author__,
    __author_email__
)


setup(
    name='odt2md',
    version=__version__,
    description=__description__,
    keywords=__keywords__,
    url=__url__,
    author=__author__,
    author_email=__author_email__,

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Religion',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],

    packages=find_packages(),

    install_requires=['regex', 'lxml', 'lxmlx'],

    entry_points={
        'console_scripts': [
            'odt2md=odt2md.odt2md:main',
            'show_styles=odt2md.show_styles:main'
        ],
    },
)
