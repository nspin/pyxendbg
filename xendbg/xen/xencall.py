from collections import namedtuple

from xendbg.xen._bindings import ffi, lib
from xendbg.xen.exceptions import XenException

GDBSXDomStatus = namedtuple('GDBSXDomStatus', 'paused vcpu_id vcpu_ev')

class XenCall:

    def __init__(self):
        self.xcall = lib.xencall_open(ffi.NULL, 0)
        if self.xcall == ffi.NULL:
            raise XenException('Failed to open xencall handle', errno=True)

    def close(self):
        err = lib.xencall_close(self.xcall)
        if err != 0:
            raise XenException('Failed to close xencall handle', errno=True)
            
    def domctl(self, domid, cmd, before, after):
        buf = lib.xencall_alloc_buffer(self.xcall, ffi.sizeof('xen_domctl_t'))
        domctl = ffi.cast('xen_domctl_t *', buf)
        domctl.interface_version = lib.XEN_DOMCTL_INTERFACE_VERSION
        domctl.domain = domid
        domctl.cmd = cmd
        before(domctl.u)
        err = lib.xencall1(self.xcall, lib.FOO__HYPERVISOR_domctl, ffi.cast('uint64_t', buf))
        try:
            if err != 0:
                raise XenException('Hypercall failed with', -err)
            else:
                return after(domctl.u)
        finally:
            lib.xencall_free_buffer(self.xcall, buf)

    def domctl_gdbsx_guestmemio(self, domid, pgd3val, gva, uva, len_, gwr):
        def before(u):
            u.gdbsx_guest_memio = ffi.new('struct xen_domctl_gdbsx_memio')
            u.gdbsx_guest_memio.pgd3val = pgd3val
            u.gdbsx_guest_memio.gva = gva
            u.gdbsx_guest_memio.uva = uva
            u.gdbsx_guest_memio.len = len_
            u.gdbsx_guest_memio.gwr = gwr
        def after(u):
            return u.gdbsx_guest_memio.remain
        return self.domctl(domid, lib.XEN_DOMCTL_gdbsx_guestmemio, before, after)

    def domctl_gdbsx_pausevcpu(self, domid, vcpu):
        def before(u):
            u.gdbsx_pauseunp_vcpu.vcpu = vcpu
        def after(u):
            return None
        return self.domctl(domid, lib.XEN_DOMCTL_gdbsx_pausevcpu, before, after)

    def domctl_gdbsx_unpausevcpu(self, domid, vcpu):
        def before(u):
            u.gdbsx_pauseunp_vcpu.vcpu = vcpu
        def after(u):
            return None
        return self.domctl(domid, lib.XEN_DOMCTL_gdbsx_unpausevcpu, before, after)

    def domctl_gdbsx_domstatus(self, domid):
        def before(u):
            return
        def after(u):
            return GDBSXDomStatus(
                paused = u.gdbsx_domstatus.paused,
                vcpu_id = u.gdbsx_domstatus.vcpu_id,
                vcpu_ev = u.gdbsx_domstatus.vcpu_ev,
                )
        return self.domctl(domid, lib.XEN_DOMCTL_gdbsx_domstatus, before, after)
