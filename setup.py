import os
import sys
import platform

from setuptools import setup, find_packages, Extension

setup(
    name='pytreesitter',
    packages=['pytreesitter'],
    ext_package='pytreesitter',
    ext_modules = [
        Extension(
            "_binding",
            [
                "src/tree-sitter/lib/src/lib.c",
                "src/binding.i"
            ],
            include_dirs = [
                "src/tree-sitter/lib/include",
                "src/tree-sitter/lib/utf8proc",
            ],
            swig_opts = [
                "-Isrc/tree-sitter/lib/include",
                "-Isrc/tree-sitter/lib/utf8proc",
            ],
            extra_compile_args = (
                ['-std=c99'] if platform.system() != 'Windows' else None
            )
        )
    ],
)
