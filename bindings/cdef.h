#define XENVER_version ...

#define FOO__HYPERVISOR_domctl ...

#define XEN_DOMCTL_INTERFACE_VERSION ...

#define XEN_DOMCTL_gdbsx_guestmemio ...
#define XEN_DOMCTL_gdbsx_pausevcpu ...
#define XEN_DOMCTL_gdbsx_unpausevcpu ...
#define XEN_DOMCTL_gdbsx_domstatus ...

typedef int... domid_t;
typedef uint8_t xen_domain_handle_t[16];

typedef int... uint64_aligned_t;

struct xen_arch_domainconfig {
    uint32_t emulation_flags;
};

/* XEN_DOMCTL_gdbsx_guestmemio      guest mem io */
struct xen_domctl_gdbsx_memio {
    /* IN */
    uint64_aligned_t pgd3val;/* optional: init_mm.pgd[3] value */
    uint64_aligned_t gva;    /* guest virtual address */
    uint64_aligned_t uva;    /* user buffer virtual address */
    uint32_t         len;    /* number of bytes to read/write */
    uint8_t          gwr;    /* 0 = read from guest. 1 = write to guest */
    /* OUT */
    uint32_t         remain; /* bytes remaining to be copied */
};

/* XEN_DOMCTL_gdbsx_pausevcpu */
/* XEN_DOMCTL_gdbsx_unpausevcpu */
struct xen_domctl_gdbsx_pauseunp_vcpu { /* pause/unpause a vcpu */
    uint32_t         vcpu;         /* which vcpu */
};

/* XEN_DOMCTL_gdbsx_domstatus */
struct xen_domctl_gdbsx_domstatus {
    /* OUT */
    uint8_t          paused;     /* is the domain paused */
    uint32_t         vcpu_id;    /* any vcpu in an event? */
    uint32_t         vcpu_ev;    /* if yes, what event? */
};


struct xen_domctl {
    uint32_t cmd;
    uint32_t interface_version;
    domid_t domain;
    union {
        struct xen_domctl_gdbsx_memio gdbsx_guest_memio;
        struct xen_domctl_gdbsx_pauseunp_vcpu gdbsx_pauseunp_vcpu;
        struct xen_domctl_gdbsx_domstatus gdbsx_domstatus;
        uint8_t pad[128];
        /* ...; */
    } u;
};
typedef struct xen_domctl xen_domctl_t;

typedef ... xentoollog_logger;

/* <xenctrl.h> */

typedef ... xc_interface;

typedef struct {
    uint32_t      domid;
    uint32_t      ssidref;
    unsigned int  dying:1, crashed:1, shutdown:1,
                  paused:1, blocked:1, running:1,
                  hvm:1, debugged:1, xenstore:1, hap:1;
    unsigned int  shutdown_reason; /* only meaningful if shutdown==1 */
    unsigned long nr_pages; /* current number, not maximum */
    unsigned long nr_outstanding_pages;
    unsigned long nr_shared_pages;
    unsigned long nr_paged_pages;
    unsigned long shared_info_frame;
    uint64_t      cpu_time;
    unsigned long max_memkb;
    unsigned int  nr_online_vcpus;
    unsigned int  max_vcpu_id;
    xen_domain_handle_t handle;
    unsigned int  cpupool;
    struct xen_arch_domainconfig arch_config;
} xc_dominfo_t;

struct cpu_user_regs {
    uint64_t r15;
    uint64_t r14;
    uint64_t r13;
    uint64_t r12;
    uint64_t rbp;
    uint64_t rbx;
    uint64_t r11;
    uint64_t r10;
    uint64_t r9;
    uint64_t r8;
    uint64_t rax;
    uint64_t rcx;
    uint64_t rdx;
    uint64_t rsi;
    uint64_t rdi;
    uint64_t rip;
    uint16_t cs;
    uint8_t  saved_upcall_mask;
    uint64_t rflags;
    uint64_t rsp;
    uint16_t ss;
    uint16_t es;
    uint16_t ds;
    uint16_t fs;
    uint16_t gs;
    ...;
};
typedef struct cpu_user_regs cpu_user_regs_t;

struct trap_info {
    uint8_t       vector;  /* exception vector                              */
    uint8_t       flags;   /* 0-3: privilege level; 4: clear event enable?  */
    uint16_t      cs;      /* code selector                                 */
    unsigned long address; /* code offset                                   */
};
typedef struct trap_info trap_info_t;

struct vcpu_guest_context {
    unsigned long flags;                    /* VGCF_* flags                 */
    struct cpu_user_regs user_regs;         /* User-level CPU registers     */
     struct trap_info trap_ctxt[256];
    unsigned long ldt_base, ldt_ents;       /* LDT (linear address, # ents) */
    unsigned long gdt_frames[16], gdt_ents; /* GDT (machine frames, # ents) */
    unsigned long kernel_ss, kernel_sp;     /* Virtual TSS (only SS1/SP1)   */
    /* NB. User pagetable on x86/64 is placed in ctrlreg[1]. */
    unsigned long ctrlreg[8];               /* CR0-CR7 (control registers)  */
    unsigned long debugreg[8];              /* DB0-DB7 (debug registers)    */
    /* Segment base addresses. */
    uint64_t      fs_base;
    uint64_t      gs_base_kernel;
    uint64_t      gs_base_user;
    ...;
};
typedef struct vcpu_guest_context vcpu_guest_context_t;

struct trap_info_x86_64 {
    uint8_t       vector;
    uint8_t       flags;
    uint16_t      cs;
    uint64_t address;
};
typedef struct trap_info_x86_64 trap_info_x86_64_t;

struct cpu_user_regs_x86_64 {
    uint64_t r15;
    uint64_t r14;
    uint64_t r13;
    uint64_t r12;
    uint64_t rbp;
    uint64_t rbx;
    uint64_t r11;
    uint64_t r10;
    uint64_t r9;
    uint64_t r8;
    uint64_t rax;
    uint64_t rcx;
    uint64_t rdx;
    uint64_t rsi;
    uint64_t rdi;
    uint64_t rip;
    uint16_t cs;
    uint8_t  saved_upcall_mask;
    uint64_t rflags;
    uint64_t rsp;
    uint16_t ss;
    uint16_t es;
    uint16_t ds;
    uint16_t fs;
    uint16_t gs;
    ...;
};
typedef struct cpu_user_regs_x86_64 cpu_user_regs_x86_64_t;

struct vcpu_guest_context_x86_64 {
    struct { char x[512]; } fpu_ctxt;
    uint64_t flags;
    struct cpu_user_regs_x86_64 user_regs;
    struct trap_info_x86_64 trap_ctxt[256];
    uint64_t ldt_base, ldt_ents;
    uint64_t gdt_frames[16], gdt_ents;
    uint64_t kernel_ss, kernel_sp;
    uint64_t ctrlreg[8];
    uint64_t debugreg[8];
    uint64_t event_callback_eip;
    uint64_t failsafe_callback_eip;
    uint64_t syscall_callback_eip;
    uint64_t vm_assist;
    uint64_t      fs_base;
    uint64_t      gs_base_kernel;
    uint64_t      gs_base_user;
};
typedef struct vcpu_guest_context_x86_64 vcpu_guest_context_x86_64_t;

typedef union
{
    vcpu_guest_context_x86_64_t x64;
    // vcpu_guest_context_x86_32_t x32;
    vcpu_guest_context_t c;
    ...;
} vcpu_guest_context_any_t;

xc_interface *xc_interface_open(xentoollog_logger *logger, xentoollog_logger *dombuild_logger, unsigned open_flags);
int xc_interface_close(xc_interface *xch);
int xc_version(xc_interface *xch, int cmd, void *arg);
int xc_domain_getinfo(xc_interface *xch, uint32_t first_domid, unsigned int max_doms, xc_dominfo_t *info);
int xc_domain_setdebugging(xc_interface *xch, uint32_t domid, unsigned int enable);
unsigned long xc_translate_foreign_address(xc_interface *xch, uint32_t dom, int vcpu, unsigned long long virt);
int xc_domain_get_guest_width(xc_interface *xch, uint32_t domid, unsigned int *guest_width);
int xc_vcpu_setcontext(xc_interface *xch, uint32_t domid, uint32_t vcpu, vcpu_guest_context_any_t *ctxt);
int xc_vcpu_getcontext(xc_interface *xch, uint32_t domid, uint32_t vcpu, vcpu_guest_context_any_t *ctxt);

/* <xencall.h> */

typedef ... xencall_handle;

xencall_handle *xencall_open(struct xentoollog_logger *logger, unsigned open_flags);
int xencall_close(xencall_handle *xcall);
void *xencall_alloc_buffer(xencall_handle *xcall, size_t size);
void xencall_free_buffer(xencall_handle *xcall, void *p);
int xencall1(xencall_handle *xcall, unsigned int op, uint64_t arg1);

/* <xenstore.h> */

#define XBT_NULL ...

struct xs_handle;
typedef uint32_t xs_transaction_t;

struct xs_handle *xs_open(unsigned long flags);
void xs_close(struct xs_handle *xsh);
xs_transaction_t xs_transaction_start(struct xs_handle *h);
bool xs_transaction_end(struct xs_handle *h, xs_transaction_t t, bool abort);
char **xs_directory(struct xs_handle *h, xs_transaction_t t, const char *path, unsigned int *num);
void *xs_read(struct xs_handle *h, xs_transaction_t t, const char *path, unsigned int *len);

/* <xenforeignmemory.h> */

#define XC_PAGE_SIZE ...
#define XC_PAGE_SHIFT ...
#define PROT_READ ...
#define PROT_WRITE ...

typedef ...  xenforeignmemory_handle;
typedef int... xen_pfn_t;

xenforeignmemory_handle *xenforeignmemory_open(struct xentoollog_logger *logger, unsigned open_flags);
int xenforeignmemory_close(xenforeignmemory_handle *fmem);
void *xenforeignmemory_map(xenforeignmemory_handle *fmem, uint32_t dom, int prot, size_t pages, const xen_pfn_t arr[/*pages*/], int err[/*pages*/]);
int xenforeignmemory_unmap(xenforeignmemory_handle *fmem, void *addr, size_t pages);

void *malloc(size_t size);
void free(void *ptr);
