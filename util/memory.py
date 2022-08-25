# Import dependencies
import psutil, resource

# Functions
def rss():
    rss_size = psutil.Process().memory_info().rss
    print(f'Resident Set Size: {convert_bytes(rss_size)}')


def virtual():
    mem = psutil.virtual_memory()
    print(f'Mem. Total:\t{convert_bytes(mem.total)}')  # total
    print(f'Mem. Available:\t{convert_bytes(mem.available)}')  # available
    print(f'Mem. Used:\t{convert_bytes(mem.used)}')  # used
    print(f'Mem. Free:\t{convert_bytes(mem.free)}')  # free
    print(f'Mem. Active:\t{convert_bytes(mem.active)}')  # active
    print(f'Mem. Inactive:\t{convert_bytes(mem.inactive)}')  # inactive
    print(f'Mem. Buffers:\t{convert_bytes(mem.buffers)}')  # buffers
    print(f'Mem. Cached:\t{convert_bytes(mem.cached)}')  # cached
    print(f'Mem. Shared:\t{convert_bytes(mem.shared)}')  # shared
    print(f'Mem. Slab:\t{convert_bytes(mem.slab)}')  # slab
    #print(f'Mem. Wired:\t{convert_bytes(mem.wired)}')  # wired (not in linux#)
    #return mem


def usage():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    for name, desc in [
        ('ru_utime', 'User time'),
        ('ru_stime', 'System time'),
        ('ru_maxrss', 'Max. Resident Set Size'),
        ('ru_ixrss', 'Shared Memory Size'),
        ('ru_idrss', 'Unshared Memory Size'),
        ('ru_isrss', 'Stack Size'),
        ('ru_inblock', 'Block inputs'),
        ('ru_oublock', 'Block outputs'),
        ]:
        print('%-25s (%-10s) = %s' % (desc, name, getattr(usage, name)))


def limits():
    for name, desc in [
        ('RLIMIT_CORE', 'core file size'),
        ('RLIMIT_CPU',  'CPU time'),
        ('RLIMIT_FSIZE', 'file size'),
        ('RLIMIT_DATA', 'heap size'),
        ('RLIMIT_STACK', 'stack size'),
        ('RLIMIT_RSS', 'resident set size'),
        ('RLIMIT_NPROC', 'number of processes'),
        ('RLIMIT_NOFILE', 'number of open files'),
        ('RLIMIT_MEMLOCK', 'lockable memory address'),
        ]:
        limit_num = getattr(resource, name)
        soft, hard = resource.getrlimit(limit_num)
        print('Maximum %-25s (%-15s) : %20s %20s' % (desc, name, soft, hard))


def convert_bytes(b):
    if b < 1024:  # less than 1kb
        label = f'{round(b,3)}bytes'
    elif b < (1024*1024):  # less than 1MB
        label = f'{round(b/(1024),3)}kB'
    elif b < (1024*1024*1024):  # less than 1GB
        label = f'{round(b/(1024*1024),3)}MB'
    elif b < (1024*1024*1024*1024):  # less than 1TB
        label = f'{round(b/(1024*1024*1024),3)}GB'
    else:  # over 1TB
        label = f'{round(b/(1024*1024*1024*1024),3)}TB'
    return label


def obj_size(obj):
    """Get the memory size of any object in bytes"""
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the objects referred to in obj_q.
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Ignore objects that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    return sz