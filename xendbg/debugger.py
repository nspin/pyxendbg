class Debugger:

    def __init__(self, domain):
        self.domain = domain
        self.breakpoints = {}

        # _on_stop
        # _vcpu_id
        # _is_attached
        # _last_stop_reason

        # _domain
        # _timer
        # _is_in_pre_continue_singlestep
        # _is_continuing

        # _last_single_step_vcpu_id
        # _last_single_step_breakpoint_addr

    def get_domain(self):
        return self.domain

    def attach(self):
        pass

    def detach(self):
        pass

    def cleanup(self):
        pass

    def continue_(self):
        pass

    def single_step(self):
        pass

    def insert_breakpoint(self, addr):
        pass

    def remove_breakpoint(self, addr):
        pass

    # virtual void insert_watchpoint(xen::Address address, uint32_t bytes, WatchpointType type);
    # virtual void remove_watchpoint(xen::Address address, uint32_t bytes, WatchpointType type);

    def on_stop(self, on_stop_fn):
        pass

    def get_last_stop_reason(self):
        return _last_stop_reason

    def read_memory_masking_breakpoints(addr, len_):
        return b''

    def write_memory_retaining_breakpoints(addr, len_, data):
        pass

    def get_vcpu_id(self):
        return self._vcpu_id

    def set_vcpu_id(self, vcpu_id):
        return self._vcpu_id = vcpu_id

    def did_stop(self, reason):
        pass
