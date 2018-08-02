from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy


# cythonize：编译源代码为C或C++，返回一个distutils Extension对象列表
setup(name='floodfill', ext_modules=cythonize([Extension("floodfill", ['floodfill.pyx'], include_dirs=[numpy.get_include()]), ]))
