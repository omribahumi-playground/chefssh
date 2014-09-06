#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='chef-ssh',
    version='0.1',
    description="Chef SSH is a tool to easily query the Chef server's inventory for running scp/ssh to/from the machines",
    author='Omri Bahumi',
    author_email='omri.il@gmail.com',
    url='https://github.com/omribahumi/chefssh',
    packages=find_packages(),
    install_requires=['PyChef>=0.2'],
    entry_points={
        'console_scripts': [
            'chef-ssh=chefssh.entry:ssh',
            'chef-scp=chefssh.entry:scp'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Clustering',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ]
)

