#!/usr/bin/env python
from setuptools import find_namespace_packages
from distutils.core import setup
import os

package_name = "dbt-bigquery"
package_version = "0.15.0b1"
description = """The bigquery adapter plugin for dbt (data build tool)"""

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Fishtown Analytics",
    author_email="info@fishtownanalytics.com",
    url="https://github.com/fishtown-analytics/dbt",
    packages=find_namespace_packages(include=['dbt.*']),
    package_data={
        'dbt': [
            'include/bigquery/dbt_project.yml',
            'include/bigquery/macros/*.sql',
            'include/bigquery/macros/**/*.sql',
        ]
    },
    install_requires=[
        'dbt-core=={}'.format(package_version),
        'google-cloud-bigquery>=1.0.0,<2',
    ]
)
