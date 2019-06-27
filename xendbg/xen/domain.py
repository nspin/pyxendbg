from xendbg.xen._bindings import ffi, lib
from xendbg.xen.vcpu import VCPU

class Domain:

    def __init__(self, xen, domid):
        self.xen = xen
        self.domid = domid

    def vcpu(self, vcpu_id):
        return VCPU(self, vcpu_id)

    def _domain_store_path(self):
        return b'/local/domain/' + str(self.domid).encode('ascii')

    def get_domid(self):
        return self.domid

    def get_name(self):
        return self.xen.xenstore.read(self._domain_store_path() + b'/name')

    def get_kernel_path(self):
        vm = self.xen.xenstore.read(self._domain_store_path() + b'/vm')
        return self.xen.xenstore.read(vm + b'/image/kernel')

    def get_dominfo(self):
        return self.xen.xenctrl.domain_getinfo(self.domid)

    def get_word_size(self):
        return self.xen.xenctrl.domain_get_guest_width(self.domid)

    def set_debugging(self, enable):
        self.xen.xenctrl.domain_setdebugging(self.domid, enable)

    # virtual void set_singlestep(bool enabled, VCPU_ID vcpu_id) const = 0;

    def translate_foreign_address(self, vaddr, vcpu):
        return self.xen.xenctrl.translate_foreign_address(self.domid, vcpu, vaddr)

    # std::optional<PageTableEntry> get_page_table_entry(Address address, VCPU_ID vcpu_id) const;

    # void set_mem_access(xenmem_access_t access, Address start_address, Address size) const;
    # xenmem_access_t get_mem_access(Address pfn) const;

    # virtual xd::reg::RegistersX86Any get_cpu_context(VCPU_ID vcpu_id) const = 0;
    # virtual void set_cpu_context(xd::reg::RegistersX86Any regs, VCPU_ID vcpu_id) const = 0;

    # void pause_vcpu(VCPU_ID vcpu_id);
    # void unpause_vcpu(VCPU_ID vcpu_id);
    # void pause_vcpus_except(VCPU_ID vcpu_id);
    # void unpause_vcpus_except(VCPU_ID vcpu_id);
    # void pause_all_vcpus();
    # void unpause_all_vcpus();

    # void pause() const;
    # void unpause() const;
    # void shutdown(int reason) const;
    # void destroy() const;

    # xen_pfn_t get_max_gpfn() const;

    # XenCall::DomctlUnion hypercall_domctl(uint32_t command, XenCall::InitFn init = {}, XenCall::CleanupFn cleanup = {}) const;

    def map_memory(self, vaddr, size, prot):
        base_mfn = self.translate_foreign_address(vaddr, 0)
        return self.xen.xenforeignmemory.map_by_mfn(self.domid, base_mfn, vaddr % lib.XC_PAGE_SIZE, size, prot)

    def map_memory_by_mfn(self, mfn, offset, size, prot):
        return self.xenforeignmemory.map_by_mfn(self.domid, mfn, offset, size, prot)

    # void set_access_required(bool required);
