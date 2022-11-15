What is annotations?
====================

annotations is a tool that allows to parse and manage kernel .config files
in annotations format (Ubuntu kernel .config format).

annotations allows to query individual .config options, architectures or
flavours and it allows to import/export settings from annotations format to
kconfig format and vice-versa.

Examples
========

Show settings for `CONFIG_DEBUG_FS` for master kernel across all the supported
architectures and flavours:
```
$ annotations --query --config CONFIG_DEBUG_FS
{
    "policy": {
        "amd64": "y",
        "arm64": "y",
        "armhf": "y",
        "ppc64el": "y",
        "riscv64": "y",
        "s390x": "y"
    },
    "note": "'required debug option'"
}
```

Dump kernel .config for arm64 and flavour generic-64k:
```
$ annotations -a arm64 -l generic-64k --export
CONFIG_DEBUG_FS=y
CONFIG_DEBUG_KERNEL=y
CONFIG_COMPAT=y
...
```

Update annotations file with a new kernel .config for amd64 flavour generic:
```
$ annotations --arch amd64 --flavour generic --import build/.config
```

TODO
====

 - Migrate arches and flavours definition to annotations
 - Automatically migrate from old annotations to new annotations format
