from distutils.core import setup
from distutils.extension import Extension
import re

# Automate 2to3 in the installation process.
try:
    from distutils.command.build_py import build_py_2to3 as build_py
    from distutils.command.build_scripts \
        import build_scripts_2to3 as build_scripts
except ImportError:
    from distutils.command.build_py import build_py
    from distutils.command.build_scripts import build_scripts


_init_preload = Extension(
    "mrhooker._init_preload",
    ["src/common.c"],
    libraries = ["dl"]
)


description = """
MrHooker is a command-line tool for hooking function calls in Cython,
using LD_PRELOAD. Hooks are written in `Cython <http://cython.org>`_ (a dialect
of Python), and compiled on the fly. MrHooker will take care of setting up the
environment, initializing Python in the child process, and cleaning up
afterwards.
""".strip()


# Get the version from lib/mrhooker/__init__.py
init_py_source = open("lib/mrhooker/__init__.py").read()
match = re.search('__version__ = "(.*)"', init_py_source)
assert match
version = match.group(1)


classifiers =[
    "Intended Audience :: Developers",
    "Operating System :: POSIX :: Linux",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 4 - Beta",
    "Programming Language :: Cython",
    "Topic :: Utilities"
]


setup(
    name="mrhooker",
    description=description,
    version=version,
    classifiers=classifiers,
    cmdclass = {"build_py": build_py, "build_scripts": build_scripts},
    packages = ["mrhooker"],
    package_dir = {"": "lib"},
    scripts = ["scripts/mrhooker"],
    ext_modules=[_init_preload],
    author="Andrew Wilkins",
    author_email="axwalk@gmail.com",
    url="http://github.com/axw/mrhooker"
)

