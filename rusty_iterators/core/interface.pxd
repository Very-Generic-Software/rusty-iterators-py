from rusty_iterators.core.async_interface cimport AsyncIterAdapter

cdef class IterInterface:
    cpdef void advance_by(self, int n)
    cpdef AsyncIterAdapter as_async(self)
    cpdef Chain chain(self, IterInterface second)
    cpdef list collect(self)
    cpdef object collect_into(self, object factory)
    cpdef IterInterface copy(self)
    cpdef int count(self)
    cpdef IterInterface cycle(self, bint use_cache = *)
    cpdef Enumerate enumerate(self)
    cpdef Flatten flatten(self)
    cpdef Filter filter(self, object func)
    cpdef object fold(self, object init, object func)
    cpdef void for_each(self, object func)
    cpdef object last(self)
    cpdef Inspect inspect(self, object f = *)
    cpdef Map map(self, object func)
    cpdef object max(self)
    cpdef object min(self)
    cpdef IterInterface moving_window(self, int size, bint use_cache = *)
    cpdef object next(self)
    cpdef object nth(self, int n)
    cpdef Peekable peekable(self)
    cpdef object product(self)
    cpdef object reduce(self, object func)
    cpdef Skip skip(self, int amount)
    cpdef StepBy step_by(self, int step)
    cpdef object sum(self)
    cpdef Take take(self, int amount)
    cpdef Unique unique(self)
    cpdef object unzip(self)
    cpdef Zip zip(self, IterInterface second)

cdef class Enumerate(IterInterface):
    cdef IterInterface it
    cdef int curr_idx

cdef class Filter(IterInterface):
    cdef IterInterface it
    cdef object func

cdef class Flatten(IterInterface):
    cdef IterInterface it
    cdef int ptr
    cdef list cache
    cdef int cache_size

cdef class Inspect(IterInterface):
    cdef IterInterface it
    cdef object f

cdef class Map(IterInterface):
    cdef IterInterface it
    cdef object func

cdef class CacheCycle(IterInterface):
    cdef IterInterface it
    cdef int ptr
    cdef bint use_cache
    cdef list cache

cdef class CacheMovingWindow(IterInterface):
    cdef IterInterface it
    cdef int size
    cdef list cache
    cdef int ptr

cdef class CopyCycle(IterInterface):
    cdef IterInterface it
    cdef IterInterface orig

cdef class CopyMovingWindow(IterInterface):
    cdef IterInterface it
    cdef IterInterface orig
    cdef int size

cdef class Peekable(IterInterface):
    cdef IterInterface it
    cdef object peeked
    cdef bint was_peeked

    cpdef object peek(self)

cdef class Skip(IterInterface):
    cdef IterInterface it
    cdef int amount

cdef class StepBy(IterInterface):
    cdef bint first_take
    cdef IterInterface it
    cdef int step_minus_one

cdef class Take(IterInterface):
    cdef IterInterface it
    cdef int taken
    cdef int amount

cdef class Unique(IterInterface):
    cdef IterInterface it
    cdef set used

cdef class Zip(IterInterface):
    cdef IterInterface first
    cdef IterInterface second

cdef class Chain(IterInterface):
    cdef IterInterface first
    cdef IterInterface second
    cdef bint use_second
