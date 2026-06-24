from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "exercicio9",          # O nome do módulo que será gerado e importado
        ["exercicio9.pyx"],    # O seu arquivo Cython
        extra_compile_args=["-fopenmp"],
        extra_link_args=["-fopenmp"],
    )
]

setup(name="exercicio9", ext_modules=cythonize(ext_modules))