#!/usr/bin/env python

from setuptools import setup

setup(
    name='cc-iaas-sdnms',
    version='1.0.0',
    description=('cc-iaas-sdnms'),
    long_description='cc-iaas-sdnms',
    license='Apache v2',
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'cc-iaas-sdnms = cc_iaas_sdnms.app.server:launch'
        ],
    },
)
