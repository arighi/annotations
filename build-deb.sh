#!/bin/bash
#
# Automatically create a deb from the git repository
#
# Requirements:
#  - apt install git-buildpackage

if [ ! -d .git ]; then
    echo "error: must be ran from a git repository"
    exit 1
fi

# Create upsteam tag
deb_tag=$(dpkg-parsechangelog -S version | cut -d- -f1)
git tag upstream/${deb_tag}

gbp buildpackage --git-ignore-branch $*

# Undo packaging changes
git tag -d upstream/${deb_tag}
