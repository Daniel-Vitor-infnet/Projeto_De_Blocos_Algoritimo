from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [ 
    Extension(
        "exercicio",
        ["exercicio.pyx"],
        extra_compile_args=["-fopenmp"],
        extra_link_args=["-fopenmp"],
    )
]

setup(
    name="exercicio", 
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': "3"})
)