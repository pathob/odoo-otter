#!/usr/bin/env python

from setuptools import find_packages, setup

from otter.const import OTTER_PACKAGE, OTTER_DESCRIPTION, OTTER_VERSION

with open("README.md", "r") as file:
    long_description = file.read()

requirements = []
with open("requirements.txt", "r") as file:
    for line in file.read().splitlines():
        if not line.strip().startswith("#"):
            requirements.append(line)

setup(
    name=OTTER_PACKAGE,
    version=OTTER_VERSION,
    description=OTTER_DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pathob/odoo-otter',
    author='Patrick Hobusch',
    author_email='pathob@users.noreply.github.com',
    license='Apache 2.0',
    packages=find_packages(),
    zip_safe=False,

    install_requires=requirements,

    entry_points={
        'console_scripts': [
            'otter=otter.otter:main'
        ],
    },
)
