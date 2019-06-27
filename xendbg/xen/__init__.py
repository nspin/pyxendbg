from xendbg.xen._bindings import ffi, lib
from xendbg.xen.exceptions import XenException
from xendbg.xen.xen import Xen

PROT_READ = lib.PROT_READ
PROT_WRITE = lib.PROT_WRITE
