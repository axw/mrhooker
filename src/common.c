/*
 * Copyright (c) 2011 Andrew Wilkins <axwalk@gmail.com>
 * 
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 * 
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

/* For RTLD_DEFAULT. */
#define _GNU_SOURCE

#include <assert.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <string.h>

static void init_mrhooker(void) __attribute__((constructor));

#define PYTHON3_MODULE_PREFIX "PyInit_"
#define PYTHON2_MODULE_PREFIX "init"

void init_mrhooker()
{
    void(*Py_Initialize_)(void);
    void(*init_module_fn)(void);
    const char *module_name;
    size_t module_name_len;
    char module[256];

    /* Initialise Python. */
    Py_Initialize_ = (void(*)(void))dlsym(RTLD_DEFAULT, "Py_Initialize");
    assert(Py_Initialize_);
    Py_Initialize_();

    /* Get the module name. */
    module_name = getenv("MRHOOKER_MODULE");
    assert(module_name);
    module_name_len = strlen(module_name);
    assert(
        (module_name_len > 0) &&
        (module_name_len + sizeof(PYTHON3_MODULE_PREFIX)-1) < sizeof(module));

    /* Look for the Python 2 format module init function. */
    memcpy(module, PYTHON2_MODULE_PREFIX, sizeof(PYTHON2_MODULE_PREFIX)-1);
    memcpy(module+sizeof(PYTHON2_MODULE_PREFIX)-1,
           module_name, module_name_len+1); /* +1 for NULL byte */
    init_module_fn = (void(*)(void))dlsym(RTLD_DEFAULT, module);

    /* If we didn't find the Python 2 module init function, look for the
     * Python 3 name format.*/
    if (!init_module_fn)
    {
        memcpy(module, PYTHON3_MODULE_PREFIX, sizeof(PYTHON3_MODULE_PREFIX)-1);
        memcpy(module+sizeof(PYTHON3_MODULE_PREFIX)-1,
               module_name, module_name_len+1); /* +1 for NULL byte */
        init_module_fn = (void(*)(void))dlsym(RTLD_DEFAULT, module);
    }

    /* Finally, initialise the module. */
    assert(init_module_fn);
    init_module_fn();
}

