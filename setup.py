"""
    ulid
    ~~~~

    Universally Unique Lexicographically Sortable Identifier

    :copyright: (c) 2017 Andrew Hawker.
    :license: Apache 2.0, see LICENSE for more details.
"""
import ast
import re


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version_regex = re.compile(r'__version__\s+=\s+(.*)')


def get_version():
    with open('ulid/__init__.py', 'r') as f:
        return str(ast.literal_eval(version_regex.search(f.read()).group(1)))


def get_long_description():
    with open('README.md') as f:
        return f.read()


setup(
    name='ulid-py',
    version=get_version(),
    author='Andrew Hawker',
    author_email='andrew.r.hawker@gmail.com',
    url='https://github.com/ahawker/ulid',
    license='Apache 2.0',
    description='Universally Unique Lexicographically Sortable Identifier',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=['ulid'],
    package_data={'ulid': ['py.typed']},
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)
