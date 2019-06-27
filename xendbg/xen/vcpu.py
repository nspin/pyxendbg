from xendbg.xen._bindings import ffi, lib

class VCPU:

    def __init__(self, domain, vcpu_id):
        self.domain = domain
        self.vcpu_id = vcpu_id

    def get_context(self):
        return self.domain.xen.xenctrl.vcpu_getcontext(self.domain.domid, self.vcpu_id)

    def set_context(self, ctx):
        return self.domain.xen.xenctrl.vcpu_setcontext(self.domain.domid, self.vcpu_id, ctx)
