# pyxendbg

This repository contains a work-in-progress debugger for paravirtualized Xen guests.
It can be used for scripting directly (i.e. as a library), but it also provides a GDB stub.
This stub does not yet have enough features to be useful.

This project is similar to and inspired by [xendbg](https://github.com/nccgroup/xendbg) from NCC Group.
I seek the capability to debug AArch64 Xen guests, and decided that it would be easier to start here than to try to fit AArch64 into that project.

If you're interested in using hypervisors to debug non-paravirtualized guests (especially with stealth debugging of malware in mind), check out [LibVMI](http://libvmi.com/) and work by [Mathieu Tarral](https://twitter.com/mtarral).
