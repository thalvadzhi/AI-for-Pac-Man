
from distutils.core import setup, Extension
import os

import_file_template = """ \
def __bootstrap__():                                             
   global __bootstrap__, __loader__, __file__                     
   import sys, pkg_resources, imp                                 
   __file__ = pkg_resources.resource_filename(__name__,'{0}.so')
   __loader__ = None; del __bootstrap__, __loader__               
   imp.load_dynamic(__name__,__file__)                            
                                                                  
if __name__ != "__main__":                                        
    __bootstrap__()                                               
"""

def setup_pacman_lib():
    # the c++ extension modules
    pacman_lib = "pacman"
    extension_mod = Extension(pacman_lib, sources=["src/pacmanmodule.cpp"], language="c++", extra_compile_args=["-O3", "-ffast-math", "-mavx2", "-mfma", "-std=c++1y"])

    setup(name = pacman_lib, ext_modules=[extension_mod])
    
    with open("ai/pacman.py".format(pacman_lib), "w") as import_file:
        import_file.write(import_file_template.format(pacman_lib))

if __name__ == '__main__':
    os.environ["CC"] = "clang++"
    os.environ["CXX"] = "clang++"
    setup_pacman_lib()
