import cython
from rusty_iterators.core.async_interface cimport AsyncIterAdapter
from cpython.list cimport PyList_SET_ITEM, PyList_New
from cpython.ref cimport Py_INCREF

cdef inline object _aggregate_sum(object acc, object x):
    return acc + x

cdef inline object _persist_last_item(object _, object x):
    return x

cdef inline object _max(object acc, object x):
    return max(acc, x)

cdef inline object _min(object acc, object x):
    return min(acc, x)

cdef inline object _product(object acc, object x):
    return acc * x

cdef class IterInterface:
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __repr__(self):
        return self.__str__()

    def all(self, f=None):
        return all(f(i) for i in self) if f else all(self)

    def any(self, f=None):
        return any(f(i) for i in self) if f else any(self)

    cpdef void advance_by(self, int n):
        if n < 0:
            raise ValueError("Amount to advance by must be greater or equal to 0.")

        for _ in range(n):
            try:
                self.next()
            except StopIteration:
                break

    cpdef AsyncIterAdapter as_async(self):
        return AsyncIterAdapter(self)

    cpdef list collect(self):
        cdef list result
        result = self.collect_into(list)
        return result

    cpdef object collect_into(self, factory):
        return factory(self)

    cpdef IterInterface copy(self):
        raise NotImplementedError

    cpdef int count(self):
        cdef int result = 0

        for _ in self:
            result += 1

        return result

    cpdef IterInterface cycle(self, bint use_cache=True):
        return CacheCycle(self) if use_cache else CopyCycle(self)

    cpdef Enumerate enumerate(self):
        return Enumerate(self)

    cpdef Filter filter(self, object func):
        return Filter(self, func)

    cpdef Flatten flatten(self):
        return Flatten(self)

    cpdef object fold(self, object init, object func):
        for item in self:
            init = func(init, item)
        return init

    cpdef void for_each(self, object func):
        for item in self:
            func(item)

    cpdef object last(self):
        # NOTE: 15.02.2025 <@uncommon-nickname>
        # This should probably be done better in the future.
        return self.reduce(_persist_last_item)

    cpdef Inspect inspect(self, object f=None):
        return Inspect(self, f)

    cpdef Map map(self, object func):
        return Map(self, func)

    cpdef object max(self):
        return self.reduce(_max)

    cpdef object min(self):
        return self.reduce(_min)

    cpdef IterInterface moving_window(self, int size, bint use_cache = True):
        return CacheMovingWindow(self, size) if use_cache else CopyMovingWindow(self, size)

    cpdef object next(self):
        raise NotImplementedError

    cpdef object nth(self, int n):
        self.advance_by(n)
        return self.next()

    cpdef Peekable peekable(self):
        return Peekable(self)

    cpdef object product(self):
        return self.reduce(_product)

    cpdef object reduce(self, object func):
        cdef object init = self.next()
        return self.fold(init, func)

    cpdef Skip skip(self, int amount):
        return Skip(self, amount)

    cpdef StepBy step_by(self, int step):
        return StepBy(self, step)

    cpdef object sum(self):
        # NOTE: 14.02.2025 <@uncommon-nickname>
        # Closure functions are not yet supported by Cython transpiler.
        return self.reduce(_aggregate_sum)

    cpdef Take take(self, int amount):
        return Take(self, amount)

    cpdef Unique unique(self):
        return Unique(self)

    cpdef object unzip(self):
        cdef list left = []
        cdef list right = []

        for left_item, right_item in self:
            left.append(left_item)
            right.append(right_item)

        return left, right

    cpdef Zip zip(self, IterInterface second):
        return Zip(self, second)

    cpdef Chain chain(self, IterInterface second):
        return Chain(self, second)

@cython.final
cdef class Enumerate(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it
        self.curr_idx = 0

    def __str__(self):
        return f"Enumerate(curr_idx={self.curr_idx}, it={self.it})"

    cpdef Enumerate copy(self):
        cdef Enumerate obj

        obj = Enumerate(self.it.copy())
        obj.curr_idx = self.curr_idx

        return obj

    cpdef object next(self):
        cdef object item

        item = self.it.next()
        result = (self.curr_idx, item)
        self.curr_idx += 1
        return result


@cython.final
cdef class Filter(IterInterface):
    def __cinit__(self, IterInterface it, object func):
        self.it = it
        self.func = func

    def __str__(self):
        return f"Filter(it={self.it})"

    cpdef Filter copy(self):
        cdef Filter obj

        obj = Filter(self.it.copy(), self.func)

        return obj

    cpdef object next(self):
        cdef object item
        while True:
            item = self.it.next()
            if self.func(item):
                return item

@cython.final
cdef class Flatten(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it
        self.ptr = 0
        self.cache = []
        self.cache_size = 0

    def __str__(self):
        return f"Flatten(it={self.it})"

    cpdef Flatten copy(self):
        cdef Flatten obj

        obj = Flatten(self.it.copy())
        obj.cache = self.cache
        obj.ptr = self.ptr
        obj.cache_size = self.cache_size

        return obj

    cpdef object next(self):
        cdef object item
        cdef object indexable_item
        cdef int i

        if self.ptr < self.cache_size:
            item = self.cache[self.ptr]
            self.ptr += 1
            return item

        self.ptr = 0
        indexable_item = self.it.next()

        self.cache_size = len(indexable_item) - 1

        self.cache = PyList_New(self.cache_size)

        for i in range(self.cache_size):
            item = indexable_item[i + 1]
            Py_INCREF(item)
            PyList_SET_ITEM(self.cache, i, item)

        return indexable_item[0]

@cython.final
cdef class Inspect(IterInterface):
    def __init__(self, it: IterInterface, f=None):
        self.it = it
        self.f = f or (lambda x: print(f"{self.it}: {x}"))

    def __str__(self):
        return f"Inspect(it={self.it})"

    cpdef Inspect copy(self):
        cdef Inspect obj

        obj = Inspect(self.it.copy(), self.f)

        return obj

    cpdef object next(self):
        cdef object item

        item = self.it.next()
        self.f(item)
        return item


@cython.final
cdef class Map(IterInterface):
    def __cinit__(self, IterInterface it, object func):
        self.it = it
        self.func = func

    def __str__(self):
        return f"Map(it={self.it})"

    cpdef Map copy(self):
        cdef Map obj

        obj = Map(self.it.copy(), self.func)

        return obj

    cpdef object next(self):
        return self.func(self.it.next())

@cython.final
cdef class CacheCycle(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it
        self.ptr = 0
        self.use_cache = False
        self.cache = []

    def __str__(self):
        return f"CycleCached(ptr={self.ptr}, cache_size={len(self.cache)}, it={self.it})"

    cpdef CacheCycle copy(self):
        cdef CacheCycle obj

        obj = CacheCycle(self.it.copy())
        obj.cache = self.cache[:]
        obj.ptr = self.ptr
        obj.use_cache = self.use_cache

        return obj

    cpdef object next(self):
        if self.use_cache:
            self.ptr = self.ptr % len(self.cache)
            item = self.cache[self.ptr]
            self.ptr += 1
            return item

        try:
            item = self.it.next()
            self.cache.append(item)
            return item

        except StopIteration:
            if len(self.cache) == 0:
                raise

            self.use_cache = True
            return self.next()

@cython.final
cdef class CacheMovingWindow(IterInterface):
    def __cinit__(self, IterInterface it, int size):
        if size <= 0:
            raise ValueError("Moving window size has to be greater or equal to one.")
        self.it = it
        self.size = size
        self.cache = []
        self.ptr = 0

    def __str__(self):
        return f"CacheMovingWindow(size={self.size}, cache={self.cache}, it={self.it})"

    cpdef CacheMovingWindow copy(self):
        cdef CacheMovingWindow obj

        obj = CacheMovingWindow(self.it.copy(), self.size)
        obj.cache = self.cache[::]
        obj.ptr = self.ptr

        return obj

    cpdef object next(self):
        cdef list result

        if len(self.cache) == self.size:
            self.ptr %= self.size
            self.cache[self.ptr] = self.it.next()
            self.ptr += 1

            result = []
            for _ in range(self.size):
                self.ptr %= self.size
                result.append(self.cache[self.ptr])
                self.ptr += 1
            return result

        for _ in range(self.size):
            self.cache.append(self.it.next())

        result = self.cache[::]
        return result


@cython.final
cdef class CopyCycle(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it.copy()
        self.orig = it

    def __str__(self):
        return f"CycleCopy(it={self.it}, orig={self.orig})"

    cpdef CopyCycle copy(self):
        cdef CopyCycle obj

        obj = CopyCycle(self.it.copy())
        obj.orig = self.orig.copy()

        return obj

    cpdef object next(self):
        try:
            return self.it.next()
        except StopIteration:
            self.it = self.orig.copy()
            return self.it.next()

@cython.final
cdef class CopyMovingWindow(IterInterface):
    def __cinit__(self, IterInterface it, int size):
        if size <= 0:
            raise ValueError("Moving window size has to be greater or equal to one.")
        self.it = it.copy()
        self.size = size
        self.orig = it

    def __str__(self):
        return f"CopyMovingWindow(size={self.size}, it={self.it}, orig={self.orig})"

    cpdef CopyMovingWindow copy(self):
        cdef CopyMovingWindow obj

        obj = CopyMovingWindow(self.it.copy(), self.size)
        obj.orig = self.orig.copy()

        return obj

    cpdef object next(self):
        cdef list result

        result = [self.it.next() for _ in range(self.size)]
        self.orig.next()
        self.it = self.orig.copy()

        return result

@cython.final
cdef class Chain(IterInterface):
    def __cinit__(self, IterInterface first, IterInterface second):
        self.first = first
        self.second = second
        self.use_second = False

    def __str__(self):
        return f"Chain(use_second={self.use_second}, first={self.first}, second={self.second})"

    cpdef Chain copy(self):
        cdef Chain obj

        obj = Chain(self.first.copy(), self.second.copy())
        obj.use_second = self.use_second

        return obj

    cpdef object next(self):
        if self.use_second:
            return self.second.next()

        try:
            return self.first.next()
        except StopIteration:
            self.use_second = True
            return self.next()

@cython.final
cdef class Peekable(IterInterface):
    def __cinit__(self, IterInterface it) -> None:
        self.it = it
        self.was_peeked = False

    def __str__(self):
        return f"Peekable(was_peeked={self.was_peeked}, peeked={self.peeked}, it={self.it})"

    cpdef Peekable copy(self):
        cdef Peekable obj

        obj = Peekable(self.it.copy())
        obj.was_peeked = self.was_peeked
        obj.peeked = self.peeked

        return obj

    cpdef object next(self):
        if self.was_peeked:
            self.was_peeked = False
            return self.peeked

        return self.it.next()

    cpdef object peek(self):
        if self.was_peeked:
            return self.peeked

        self.peeked = self.next()
        self.was_peeked = True

        return self.peeked

@cython.final
cdef class Skip(IterInterface):
    def __cinit__(self, IterInterface it, amount: int) -> None:
        self.it = it
        self.amount = amount

    def __str__(self):
        return f"Skip(amount={self.amount}), it={self.it}"

    cpdef Skip copy(self):
        cdef Skip obj = Skip(self.it.copy(), self.amount)
        return obj

    cpdef object next(self):
        cdef object item

        if self.amount > 0:
            item = self.it.nth(self.amount)
            self.amount = 0
        else:
            item = self.it.next()

        return item

@cython.final
cdef class StepBy(IterInterface):
    def __cinit__(self, IterInterface it, step: int) -> None:
        if step <= 0:
            raise ValueError("Step has to be greater than zero.")

        self.first_take = True
        self.it = it
        self.step_minus_one = step - 1

    def __str__(self):
        return f"StepBy(first_take={self.first_take}, step={self.step_minus_one + 1}, it={self.it})"

    cpdef StepBy copy(self):
        cdef StepBy obj

        obj = StepBy(self.it.copy(), self.step_minus_one + 1)
        obj.first_take = self.first_take

        return obj

    cpdef object next(self):
        cdef int step_size = 0 if self.first_take else self.step_minus_one
        self.first_take = False

        return self.it.nth(step_size)

@cython.final
cdef class Take(IterInterface):
    def __cinit__(self, IterInterface it, int amount):
        if amount <= 0:
            raise ValueError("You have to `take` at least one item.")

        self.it = it
        self.amount = amount
        self.taken = 0

    def __str__(self):
        return f"Take(amount={self.amount}, taken={self.taken}, it={self.it})"

    cpdef Take copy(self):
        cdef Take obj

        obj = Take(self.it.copy(), self.amount)
        obj.taken = self.taken

        return obj

    cpdef object next(self):
        if self.taken == self.amount:
            raise StopIteration

        cdef object item
        item = self.it.next()
        self.taken += 1
        return item

@cython.final
cdef class Zip(IterInterface):
    def __cinit__(self, IterInterface first, IterInterface second):
        self.first = first
        self.second = second

    def __str__(self):
        return f"Zip(first={self.first}, second={self.second})"

    cpdef Zip copy(self):
        cdef Zip obj

        obj = Zip(self.first.copy(), self.second.copy())

        return obj

    cpdef object next(self):
        return (self.first.next(), self.second.next())

@cython.final
cdef class Unique(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it
        self.used = set()

    def __str__(self):
        return f"Unique(it={self.it})"

    cpdef Unique copy(self):
        cdef Unique obj

        obj = Unique(self.it.copy())
        obj.used = self.used.copy()

        return obj

    cpdef object next(self):
        cdef object item

        while True:
            item = self.it.next()

            if item not in self.used:
                self.used.add(item)
                return item
