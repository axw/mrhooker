MrHooker
========

MrHooker is a command-line tool for hooking function calls in Cython,
using LD\_PRELOAD. Hooks are written in [Cython](http://cython.org) (a dialect
of Python), and compiled on the fly. MrHooker will take care of setting up the
environment, initializing Python in the child process, and cleaning up
afterwards.

MrHooker is currently only known to work on Linux. Feel free to send pull 
requests for additional platform support (presumably in src/common.c).


Installation
------------

    pip install mrhooker


Note: Pip doesn't seem to be honoring the "requires=cython" in setup.py. Until
I figure out why, you'll need to also run:

    pip install cython

(If you don't, expect to see "ImportError: No module named pyximport".)


Usage
-----

    $ mrhooker [options] <script.pyx> <command> [args]


Example Hook Script
-------------------

    # Import stuff from <dlfcn.h>
    cdef extern from "dlfcn.h":
    void* dlsym(void*, char*)
    void* RTLD_NEXT

    # Redefine "send". Must be defined "with gil", to ensure the Python GIL is
    # held when the hook is invoked. This hook doesn't do anything particularly
    # fancy -- it just prints out the arguments to 'send' and then calls the
    # original function.
    cdef extern ssize_t \
      send(int sockfd, char *buf, size_t len, int flags) with gil:
        print "====> send(%r, %r, %r, %r)" % (sockfd, buf[:len], len, flags)
        real_send = dlsym(RTLD_NEXT, "send")
        if real_send:
            with nogil:
                res = (<ssize_t(*)(int, void*, size_t, int) nogil>real_send)(
                    sockfd, buf, len, flags)
            return res
        else:
            return -1

