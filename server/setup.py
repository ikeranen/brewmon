# For compiling C implementation of PID algorithm to python module
from distutils.core import setup, Extension
 
module1 = Extension('pid', sources = ['pidmodule.c', 'pid.c'])
 
setup (name = 'PID controller',
        version = '0.1',
        description = 'First test of PID implementation',
        ext_modules = [module1])