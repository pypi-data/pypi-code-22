# This file is generated by C:\Users\wheel_builder\conda-bld\scipy_1511290648240\work\setup.py
# It contains system_info results at the time of building this package.
__all__ = ["get_info","show"]

lapack_mkl_info={'libraries': ['mkl_intel_lp64_dll', 'mkl_intel_thread_dll', 'mkl_core_dll', 'libiomp5md'], 'library_dirs': ['C:\\Users\\wheel_builder\\envs\\py3\\Library\\lib'], 'define_macros': [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)], 'include_dirs': ['C:\\Users\\wheel_builder\\envs\\py3\\include']}
lapack_opt_info={'libraries': ['mkl_intel_lp64_dll', 'mkl_intel_thread_dll', 'mkl_core_dll', 'libiomp5md'], 'library_dirs': ['C:\\Users\\wheel_builder\\envs\\py3\\Library\\lib'], 'define_macros': [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)], 'include_dirs': ['C:\\Users\\wheel_builder\\envs\\py3\\include']}
blas_mkl_info={'libraries': ['mkl_intel_lp64_dll', 'mkl_intel_thread_dll', 'mkl_core_dll', 'libiomp5md'], 'library_dirs': ['C:\\Users\\wheel_builder\\envs\\py3\\Library\\lib'], 'define_macros': [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)], 'include_dirs': ['C:\\Users\\wheel_builder\\envs\\py3\\include']}
blas_opt_info={'libraries': ['mkl_intel_lp64_dll', 'mkl_intel_thread_dll', 'mkl_core_dll', 'libiomp5md'], 'library_dirs': ['C:\\Users\\wheel_builder\\envs\\py3\\Library\\lib'], 'define_macros': [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)], 'include_dirs': ['C:\\Users\\wheel_builder\\envs\\py3\\include']}

def get_info(name):
    g = globals()
    return g.get(name, g.get(name + "_info", {}))

def show():
    for name,info_dict in globals().items():
        if name[0] == "_" or type(info_dict) is not type({}): continue
        print(name + ":")
        if not info_dict:
            print("  NOT AVAILABLE")
        for k,v in info_dict.items():
            v = str(v)
            if k == "sources" and len(v) > 200:
                v = v[:60] + " ...\n... " + v[-60:]
            print("    %s = %s" % (k,v))
    