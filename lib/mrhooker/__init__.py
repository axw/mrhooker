#!/usr/bin/env python

# Copyright (c) 2011 Andrew Wilkins <axwalk@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

__version__ = "0.1"

import os
import sys


def run(script, args, build_dir=None, verbose=False):
    """
    The main MrHooker entry function.

    @param script The .pyx script file used to build the LD_PRELOAD library.
    @param args The command to execute as a subprocess.
    @param build_dir The build directory, into which shared libraries are
                    stored. If this is None, then the library will be built in
                    a temporary directory and discarded at exit. Otherwise, the
                    directory will keep the build directories.
    """

    if verbose:
        print "Script path:    ", script
        print "Command:        ", args
        if build_dir is None:
            print "Build directory:", build_dir, "(temporary directory)"
        else:
            print "Build directory:", build_dir

    # Locate libpython, in the likely event that the child process does not
    # load Python itself.
    import sysconfig
    libpython = "/".join(sysconfig.get_config_vars("LIBPL", "LDLIBRARY"))

    # Locate the "_init_preload" shared library.
    import imp
    (file_, _init_preload, desc) = imp.find_module("_init_preload", __path__)

    tempdir = None
    if not build_dir:
        # Create a temporary directory to store the shared library in. We'll
        # delete it when we're done.
        import tempfile
        tempdir = tempfile.mkdtemp()
        build_dir = tempdir

    try:
        from pyximport import pyxbuild
        out_fname = pyxbuild.pyx_to_dll(
            script, build_in_temp=True, pyxbuild_dir=build_dir)

        env = os.environ.copy()
        env["LD_PRELOAD"] = " ".join([libpython, out_fname, _init_preload])
        env["MRHOOKER_MODULE"] = os.path.splitext(os.path.basename(script))[0]
        if verbose:
            print "Executing command with:\n" + \
                  "    LD_PRELOAD      =", env["LD_PRELOAD"] + "\n" + \
                  "    MRHOOKER_MODULE =", env["MRHOOKER_MODULE"] + "\n"

        import subprocess
        rc = subprocess.call(args, env=env)
        if verbose:
            print "Command completed with return code '%d'" % rc
        return rc
    finally:
        if tempdir:
            import shutil
            shutil.rmtree(tempdir)

