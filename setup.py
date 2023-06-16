#!/usr/bin/env python3

import os
import subprocess
from glob import glob
from setuptools import setup, Command
from kconfig.version import VERSION


class LintCommand(Command):
    description = "Run coding style checks"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for cmd in ("flake8", "pylint"):
            command = [cmd]
            for pattern in ("*.py", "kconfig/*.py"):
                command += glob(pattern)
            subprocess.call(command)


setup(
    name="annotations",
    version=VERSION,
    author="Andrea Righi",
    author_email="andrea.righi@canonical.com",
    description="Manage Ubuntu kernel .config",
    url="https://git.launchpad.net/~arighi/+git/annotations-tools",
    license="GPLv2",
    long_description=open(  # pylint: disable=consider-using-with
        os.path.join(os.path.dirname(__file__), "README.md"),
        "r",
        encoding="utf-8",
    ).read(),
    long_description_content_type="text/x-rts",
    packages=["kconfig"],
    install_requires=["argcomplete"],
    entry_points={
        "console_scripts": [
            "annotations = kconfig.run:main",
            "sanitize-annotations = kconfig.sanitize:main",
        ]
    },
    cmdclass={
        "lint": LintCommand,
    },
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
