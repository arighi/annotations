# Ubuntu Kernel Annotations

## Overview

Ubuntu provides a wide variety of kernels for many different architectures and
flavours, such as generic, lowlatency, cloud kernels, kvm, etc.

Maintaining a separate `.config` for each of these kernels would be extremely
challenging, Kconfig options need to always match the desired value in order to
have a kernel functional for the scope that it was designed for.

Starting with Ubuntu 22.04 (Jammy Jellyfish) the kernel team introduced a new
format of annotations: a JSON-like file to store all the kernel config options
for the supported architectures and flavours.

## Quick start

Generate the Ubuntu kernel .config for a specific architecture & flavour
(i.e., `amd64`, `generic`):

```
$ annotations --arch amd64 --flavour generic --export > .config
```

Import your own kernel .config in the Ubuntu kernel for a specific architecture
and flavour (i.e., `amd64`, `generic`):

```
$ annotations --arch amd64 --flavour generic --import .config
```

After a new config is imported run `fakeroot debian/rules clean updateconfigs`
to update the dependencies, then you can review the actual changes doing a
simple `git diff`.

## Ubuntu kernel annotations

There is a main annotations file for each Ubuntu kernel in:
`debian.<kernel_name>/config/annotations`

The main annotations file can include other annotations (recursively).

The annotations has 4 different sections:

 - a header (that defines the format version, the list of supported
   architectures, the list of supported flavours paired with each architecture
   and a list of flavour inheritance rules)

 - a list of includes (annotations can include other annotations files to
   create a hierarchy of configs with overrides)

 - a subset of mandatory config options that have a note associated (typically
   config options that must be enforced for certain reasons, the note can be
   simply a reference to a tracking bug, explaining why the specific config
   needs to be set to a certain value, or just a description, like security
   implications for that config value, etc.)

 - a subset of config options that are either generated as dependency of the
   previous subset of configs or configs that have been set using the default
   Ubuntu policy (enable everything as module when possible, except for debugging,
   testing or deprecated features), so they don't need an explicit note.

The annotations format looks like the following:

```
# Menu: HEADER
# FORMAT: 4
# ARCH: <ARCH_1> <ARCH_2> <ARCH_3> ... <ARCH_N>
# FLAVOUR: <ARCH_1>-<FLAVOUR_1> <ARCH1_FLAVOUR_2> ... <ARCH_N>-<FLAVOUR_M>
# FLAVOUR_DEP: {'<ARCH_1>-<FLAVOUR_1>': '<PARENT_ARCH_1>-<PARENT_FLAVOUR_1>', ..., '<ARCH_N>-<FLAVOUR_M>': '<PARENT_ARCH_N>-<PARENT_FLAVOUR_M>'}

include <FILE_1>
include <FILE_2>
...
include <FILE_N>

CONFIG_<FOO>                                  policy<{'<ARCH_1>[-<FLAVOUR_1>]': '<VALUE_1_1>', ..., '<ARCH_N>[-<FLAVOUR_M>]': '<VALUE_N_M>'}>
CONFIG_<FOO>                                  note<'<DESCRIPTION>'>
...

# ---- Annotations without notes ----

CONFIG_<BAR>                                  policy<{'<ARCH_1>[-<FLAVOUR_1>]': '<VALUE_1_1>', ..., '<ARCH_N>[-<FLAVOUR_M>]': '<VALUE_N_M>'}>
...

```

 - **ARCH**: contains the list of comma-separated values that defines all the
   supported architectures for this kernel

 - **FLAVOUR**: contains the list of comma-separated values that defines the
   list of flavours associated to each supported architecture

 - **FLAVOUR_DEP**: contains a mapping of `ARCH-FLAVOUR` pairs mapped to a
   parent `ARCH-FLAVOUR` pair; this can be used to define flavours that derives
   from other flavours, for example `amd64-lowlatency` derives from
   `amd64-generic` (then the local annotations file will only contain an
   include rule of the generic kernel plus the small subset of config options
   to override the defaults from `amd64-generic`)

 - **FILE_1 .. FILE_N**: are the other included annotations (e.g., used by
   derivative kernels that want to include the annotations from the kernel they
   derive from)

 - **FOO, BAR**: kernel config options with the associated values across
   architectures and flavours, represented by the `policy<...>` definition

A simple example of an annotations file is the following (from the
`lunar/linux-lowlatency` kernel, that derives from the generic kernel
`lunar/linux`):

```
# Menu: HEADER
# FORMAT: 4
# ARCH: amd64 arm64
# FLAVOUR: amd64-lowlatency arm64-lowlatency arm64-lowlatency-64k
# FLAVOUR_DEP: {'amd64-lowlatency': 'amd64-generic', 'arm64-lowlatency': 'arm64-generic', 'arm64-lowlatency-64k': 'arm64-generic-64k'}

include "../../debian.master/config/annotations"

CONFIG_HZ_1000                                  policy<{'amd64': 'y', 'arm64': 'y'}>
CONFIG_HZ_1000                                  note<'HZ for lowlatency must be set to 1000 to provide better system responsiveness'>

CONFIG_HZ_250                                   policy<{'amd64': 'n', 'arm64': 'n'}>
CONFIG_HZ_250                                   note<'Override default HZ used in generic'>

CONFIG_LATENCYTOP                               policy<{'amd64': 'y', 'arm64': 'y'}>
CONFIG_LATENCYTOP                               note<'https://lists.ubuntu.com/archives/kernel-team/2014-July/045006.html, LP#1655986'>

CONFIG_PREEMPT                                  policy<{'amd64': 'y', 'arm64': 'y'}>
CONFIG_PREEMPT                                  note<'Enable fully preemptible kernel'>

CONFIG_PREEMPT_VOLUNTARY                        policy<{'amd64': 'n', 'arm64': 'n'}>
CONFIG_PREEMPT_VOLUNTARY                        note<'Disable voluntary preemption model'>


# ---- Annotations without notes ----

CONFIG_HZ                                       policy<{'amd64': '1000', 'arm64': '1000'}>
```

## Managing the annotations file

To help the management of annotations each Ubuntu kernel provides a helper
script in `debian/scripts/misc/annotations` (use `--help` for an overview of
the supported actions).

Here some typical examples of what you can do with the annotations script:

 - Show settings for `CONFIG_DEBUG_INFO_BTF` for master kernel across all the
   supported architectures and flavours:

```
$ annotations --config CONFIG_DEBUG_INFO_BTF
{
    "policy": {
        "amd64": "y",
        "arm64": "y",
        "armhf": "n",
        "ppc64el": "y",
        "riscv64": "y",
        "s390x": "y"
    },
    "note": "'Needs newer pahole for armhf'"
}
```

 - Dump kernel `.config` for `arm64` and flavour `generic-64k`:

```
$ annotations --arch arm64 --flavour generic-64k --export
CONFIG_DEBUG_FS=y
CONFIG_DEBUG_KERNEL=y
CONFIG_COMPAT=y
...
```

 - Update annotations file with a new kernel .config for `amd64` flavour
   `generic`:

```
$ annotations --arch amd64 --flavour generic --import .config
```

 - Enable `CONFIG_PROVE_LOCKING` on `amd64` for flavour `generic`:

```
$ annotations -c CONFIG_PROVE_LOCKING --arch amd64 --flavour generic --write y
{
    "CONFIG_PROVE_LOCKING": {
        "policy": {
            "amd64": "y",
            "arm64": "n",
            "armhf": "n",
            "ppc64el": "n",
            "riscv64": "n",
            "s390x": "n"
        },
        "oneline": false,
        "note": "'prove locking enabled as a test'"
    }
}

$ git diff
diff --git a/debian.master/config/annotations b/debian.master/config/annotations
index 24cec55b1b20b..e331bbd6de640 100644
--- a/debian.master/config/annotations
+++ b/debian.master/config/annotations
@@ -483,6 +483,9 @@ CONFIG_PPC_SECVAR_SYSFS                         note<'LP: #1866909'>
 CONFIG_PREEMPT_NONE                             policy<{'amd64': 'n', 'arm64': 'n', 'armhf': 'n', 'ppc64el': 'n', 'riscv64': 'n', 's390x': 'y'}>
 CONFIG_PREEMPT_NONE                             note<'LP: #1543165'>
 
+CONFIG_PROVE_LOCKING                            policy<{'amd64': 'y', 'arm64': 'n', 'armhf': 'n', 'ppc64el': 'n', 'riscv64': 'n', 's390x': 'n'}>
+CONFIG_PROVE_LOCKING                            note<'prove locking enabled as a test'>
+
 CONFIG_PSI_DEFAULT_DISABLED                     policy<{'amd64': 'n', 'arm64': 'n', 'armhf': 'n', 'ppc64el': 'n', 'riscv64': 'n', 's390x': 'y'}>
 CONFIG_PSI_DEFAULT_DISABLED                     note<'LP: #1876044'>
 
@@ -9892,7 +9895,6 @@ CONFIG_PROFILE_ALL_BRANCHES                     policy<{'riscv64': 'n'}>
 CONFIG_PROFILE_ANNOTATED_BRANCHES               policy<{'amd64': 'n', 'arm64': 'n', 'armhf': 'n', 'ppc64el': 'n', 'riscv64': 'n', 's390x': 'n'}>
 CONFIG_PROFILING                                policy<{'amd64': 'y', 'arm64': 'y', 'armhf': 'y', 'ppc64el': 'y', 'riscv64': 'y', 's390x': 'y'}>
 CONFIG_PROTECTED_VIRTUALIZATION_GUEST           policy<{'s390x': 'y'}>
-CONFIG_PROVE_LOCKING                            policy<{'amd64': 'n', 'arm64': 'n', 'armhf': 'n', 'ppc64el': 'n', 'riscv64': 'n', 's390x': 'n'}>
 CONFIG_PROVIDE_OHCI1394_DMA_INIT                policy<{'amd64': 'n'}>
 CONFIG_PRU_REMOTEPROC                           policy<{'arm64': 'm', 'armhf': 'm'}>
 CONFIG_PSAMPLE                                  policy<{'amd64': 'm', 'arm64': 'm', 'armhf': 'm', 'ppc64el': 'm', 'riscv64': 'm', 's390x': 'm'}>
```

Every time the annotations file is changed we need to make sure that all the
dependent config options are refreshed.

To do so we need to run the following command:

```
$ fakeroot debian/rules clean updateconfigs
...
```

This command will take care of interfacing with the kernel Kconfig subsystem
and it will interactively ask the value for all the potentially new enabled
dependent options.

## Conclusion

The annotations format introduced in Lunar provides an easier and more
efficient way of managing kernel .config's across the large variety of kernels,
architectures and flavours that Ubuntu supports.

If you want to submit a patch to kernel-team@lists.ubuntu.com that needs to
change the kernel `.config`, or simply if you want to recompile the Ubuntu
kernel using a different `.config` you just need to modify the annotations file
and then you can simply upload your custom modified kernel to a ppa to test it,
or you can recompile it locally using the typical Ubuntu way of rebuilding
packages.

## See also

 - https://lists.ubuntu.com/archives/kernel-team/2023-June/140230.html
 - https://discourse.ubuntu.com/t/kernel-configuration-in-ubuntu/35857
