from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "exercicio9",          
        ["exercicio9.pyx"],    
        extra_compile_args=["-fopenmp"],
        extra_link_args=["-fopenmp"],
    )
]

setup(name="exercicio9", ext_modules=cythonize(ext_modules))