import errno

from xendbg.xen._bindings import ffi, lib

class XenException(Exception):

    def __init__(self, *args, errno=False):
        super().__init__(*args)
        if errno:
            self.errno = ffi.errno
        else:
            self.errno = None

    def __str__(self):
        ret = super().__str__()
        if self.errno is not None:
            ret += ' (errno = {} {})'.format(self.errno, errno.errorcode.get(self.errno))
        return ret
