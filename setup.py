# -*- coding: utf8 -*-
import os

from setuptools import setup, find_packages
from imgur import __version__
from imgur.utils import get_version


version = get_version(__version__)
long_desc = ''
requirements = []
with open('README.md') as f:
    long_desc = f.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='imgur',
    version=version,
    author='Dogeek',
    author_email='dogeek@users-noreply.github.com',
    url='https://github.com/dogeek/imgur',
    description='A python wrapper around imgur.com\'s API.',
    long_description=long_desc,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(),
    install_requires=requirements,
    license='MIT License',
    zip_safe=True,
    platforms='any',
    python_requires='>=3.7',
)