from xendbg.xen._bindings import ffi, lib
from xendbg.xen.exceptions import XenException

class XenForeignMemory:

    def __init__(self):
        self.fmem = lib.xenforeignmemory_open(ffi.NULL , 0)
        if self.fmem == ffi.NULL:
            raise XenException('failed to open xen foreign memory handle', errno=True)

    def close(self):
        err = lib.xenforeignmemory_close(self.fmem)
        if err:
            raise XenException('failed to close xen foreign memory handle:', err, errno=True)

    def map_by_mfn(self, domid, base_mfn, offset, size, prot):
        num_pages = (size + lib.XC_PAGE_SIZE - 1) >> lib.XC_PAGE_SHIFT
        pages = ffi.new('xen_pfn_t[]', [ base_mfn + i for i in range(num_pages) ])
        mem_page_base = lib.xenforeignmemory_map(self.fmem, domid, prot, num_pages, pages, ffi.NULL)
        if mem_page_base == ffi.NULL:
            raise XenException('failed to map xen foreign memory', errno=True)
        def cleanup():
            err = lib.xenforeignmemory_unmap(self.fmem, mem_page_base, num_pages)
            if err:
                raise XenException('failed to unmap xen foreign memory', mem_page_base, 'with err',  err, errno=True)
        return mem_page_base + offset, cleanup
