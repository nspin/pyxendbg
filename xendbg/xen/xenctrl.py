from collections import namedtuple

from xendbg.xen._bindings import ffi, lib
from xendbg.xen.exceptions import XenException

XenVersion = namedtuple('XenVersion', 'major minor')

class XenCtrl:

    def __init__(self):
        self.xch = lib.xc_interface_open(ffi.NULL, ffi.NULL, 0)
        if self.xch == ffi.NULL:
            raise XenException('Failed to open xenctrl handle', errno=True)

    def close(self):
        err = lib.xc_interface_close(self.xch)
        if err != 0:
            raise XenException('Failed to close xenctrl handle', errno=True)

    def version(self):
        version = lib.xc_version(self.xch, lib.XENVER_version, ffi.NULL)
        return XenVersion(
            major = version >> 16,
            minor = version & ((1 << 16) - 1),
            )

    def domain_getinfo(self, domid):
        dominfo = ffi.new('xc_dominfo_t *')
        n = lib.xc_domain_getinfo(self.xch, domid, 1, dominfo)
        if n != 1:
            raise XenException('Failed to get domain info', errno=True)
        return dominfo

    def domain_setdebugging(self, domid, enable):
        err = lib.xc_domain_setdebugging(self.xch, domid, enable)
        if err != 0:
            raise XenException('Failed to set debugging to', enable, 'for domid', domid, errno=True)

    def translate_foreign_address(self, domid, vcpu, virt):
        mfn = lib.xc_translate_foreign_address(self.xch, domid, vcpu, virt)
        if mfn == 0:
            raise XenException('Failed to translate foreign address', errno=True)
        return mfn

    def domain_get_guest_width(self, domid):
        word_size = ffi.new('unsigned int *')
        err = lib.xc_domain_get_guest_width(self.xch, domid, word_size)
        if err != 0:
            raise XenException('Failed to get word size for domain', self.domid, 'with err =', err, errno=True)
        return word_size[0]

    def vcpu_setcontext(self, domid, vcpu, ctxt):
        err = lib.xc_vcpu_setcontext(self.xch, domid, vcpu, ctxt)
        if err != 0:
            raise XenException('Failed to set vcpu context', errno=True)

    def vcpu_getcontext(self, domid, vcpu):
        ctxt = ffi.new('vcpu_guest_context_any_t *')
        err = lib.xc_vcpu_getcontext(self.xch, domid, vcpu, ctxt)
        if err != 0:
            raise XenException('Failed to get vcpu context', errno=True)
        return ctxt
