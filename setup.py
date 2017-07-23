import os.path
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as _build_ext
import warnings
'''
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

classifiers = [
    'Programming Language :: Python :: 2',
]


class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


ext = '.pyx' if USE_CYTHON else '.cpp'

extensions = [Extension(
        'CHT',
        [os.path.join('fastdtw', '_fastdtw' + ext)],
        language="c++",
        include_dirs=[],
        libraries=["stdc++"]
    )]

if USE_CYTHON:
    extensions = cythonize(extensions)
'''
kwargs = {
    'name': 'CHT',
    'version': '0.1.0',
    'description': 'transportation mode detection in cellular data',
    'keywords': ['CHT'],
    'install_requires': ['numpy','simplejson','rtree','urllib','pandas'],
    'packages': find_packages(),
    'test_suite': 'tests',
    'setup_requires': ['pytest-runner'],
    'tests_require': ['pytest'],
}

setup(**kwargs)
