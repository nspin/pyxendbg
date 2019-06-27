from cffi import FFI
from pathlib import Path

def read_local_file(path):
    return (Path(__file__).parent / path).read_text()

libraries = [
    'xenctrl',
    'xencall',
    'xenlight',
    'xendevicemodel',
    'xenevtchn',
    'xenforeignmemory',
    'xenguest',
    'xenstore',
    ]

c_header_source = r'''
    #include <xenctrl.h>
    #include <xencall.h>
    #include <libxl.h>
    #include <xendevicemodel.h>
    #include <xenevtchn.h>
    #include <xenforeignmemory.h>
    #include <xenguest.h>
    #include <xenstore.h>

    #include <xen/domctl.h>
    #include <xen/vm_event.h>
    #include <xen/io/ring.h>
    #include <xen/sys/privcmd.h>

    #include <sys/mman.h>
    #define FOO__HYPERVISOR_domctl __HYPERVISOR_domctl
'''
    #include <xentoollog.h>

cdef = read_local_file('cdef.h')

ffi = FFI()
ffi.set_source('xendbg.xen._bindings', c_header_source, libraries=libraries)
ffi.cdef(cdef)

if __name__ == '__main__':
    ffi.compile(verbose=True)
