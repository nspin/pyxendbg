from xendbg.xen.exceptions import XenException
from xendbg.xen.xenctrl import XenCtrl
from xendbg.xen.xencall import XenCall
from xendbg.xen.xenstore import XenStore
from xendbg.xen.xenforeignmemory import XenForeignMemory
from xendbg.xen.domain import Domain

class Xen:

    def __init__(self):
        self.resources = []
        try:
            self.xenctrl = XenCtrl()
            self.xencall = XenCall()
            self.xenstore = XenStore()
            self.xenforeignmemory = XenForeignMemory()
        finally:
            self.close()

    def close(self):
        def f(i):
            if i < len(self.resources):
                try:
                    self.resources[i].close
                finally:
                    f(i + 1)
        f(0)

    def domain_from_domid(self, domid):
        return Domain(self, domid)

    def domain_from_name(self, name):
        for domid in self.xenstore.directory(b'/local/domain'):
            if name == self.xenstore.read(b'/local/domain/' + domid + b'/name'):
                return self.domain_from_domid(int(domid))
        return None
