from xendbg.xen._bindings import ffi, lib
from xendbg.xen.exceptions import XenException

class XenStore:

    def __init__(self):
        self.xsh = lib.xs_open(0)
        if self.xsh == ffi.NULL:
            raise XenException('failed to open xen store handle', errno=True)

    def close(self):
        lib.xs_close(self.xsh)

    def directory(self, path):
        num_entries = ffi.new('unsigned int *')
        entries = lib.xs_directory(self.xsh, lib.XBT_NULL, path, num_entries)
        if entries == ffi.NULL:
            raise XenException('failed to read directory', path, errno=True)
        return [ ffi.string(entries[i]) for i in range(num_entries[0]) ]

    def read(self, path):
        transaction = lib.xs_transaction_start(self.xsh)
        contents = ffi.cast('char *', lib.xs_read(self.xsh, transaction, path, ffi.NULL))
        lib.xs_transaction_end(self.xsh, transaction, False)
        if contents == ffi.NULL:
            raise XenException('failed to read file', path, errno=True)
        return ffi.string(contents)
