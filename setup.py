import io
import os
import re
import setuptools


def _read(*names, **kwargs):
    # Credits: https://packaging.python.org/single_source_version.
    here = os.path.dirname(__file__)
    encoding = kwargs.get('encoding', 'utf8')
    with io.open(os.path.join(here, *names), encoding=encoding) as fp:
        return fp.read()


def _find_version(*file_paths):
    # Credits: https://packaging.python.org/single_source_version.
    version_file = _read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find the version string.")


setuptools.setup(
    name='gorilla',
    version=_find_version('gorilla.py'),
    description="Convenient approach to monkey patching",
    long_description=_read('README.rst'),
    keywords='gorilla monkey patch',
    license='MIT',
    url='https://github.com/christophercrouzet/gorilla',
    author="Christopher Crouzet",
    author_email='christopher.crouzet@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    extras_require={
        'dev': ['coverage', 'sphinx>=1.3', 'tox'],
        'docs': ['sphinx>=1.3'],
    },
    packages=[],
    py_modules=['gorilla'],
    include_package_data=True
)
