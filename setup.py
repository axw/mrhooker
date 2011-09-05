from distutils.core import setup
from distutils.extension import Extension

_init_preload = Extension(
    "mrhooker._init_preload",
    ["src/common.c"],
    libraries = ["dl"]
)

classifiers =[
    "Intended Audience :: Developers",
    "Operating System :: Linux",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 3 - Alpha",
]

setup(
    name="mrhooker",
    version="0.1",
    classifiers=classifiers,
    packages = ["mrhooker"],
    package_dir = {"": "lib"},
    scripts = ["scripts/mrhooker"],
    ext_modules=[_init_preload],
    author="Andrew Wilkins",
    author_email="axwalk@gmail.com",
    url="http://github.com/axw/mrhooker"
)

