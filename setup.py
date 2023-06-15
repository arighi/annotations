#!/usr/bin/env python3

import os
from setuptools import setup
from kconfig.version import VERSION

setup(
    name="annotations",
    version=VERSION,
    author="Andrea Righi",
    author_email="andrea.righi@canonical.com",
    description="Manage Ubuntu kernel .config",
    url="https://git.launchpad.net/~arighi/+git/annotations-tools",
    license="GPLv2",
    long_description=open(
        os.path.join(os.path.dirname(__file__), "README.rst"), "r"
    ).read(),
    long_description_content_type="text/x-rts",
    packages=["kconfig"],
    install_requires=["argcomplete"],
    entry_points={
        "console_scripts": [
            "annotations = kconfig.run:main",
        ]
    },
    scripts=[
        "bin/sanitize-annotations",
    ],
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
    ],
    zip_safe=False,
)
