# auto-generated file
__all__ = ['lib', 'ffi']

import os
from vdirsyncer._native__ffi import ffi

lib = ffi.dlopen(os.path.join(os.path.dirname(__file__), '_native__lib.so'), 4096)
del os
