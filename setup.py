# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

PACKAGES = find_packages()
INSTALL_REQUIRES = [
    'Django>=1.3',
]
setup(
    name='django-debug-utils',
    version='0.0.2',
    description='Little tools useful for debugging',
    author = "Eric Holscher",
    author_email = "eric@ericholscher.com",
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
)
