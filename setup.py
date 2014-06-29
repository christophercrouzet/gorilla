import codecs
import os
import re
import setuptools


# Taken from `Python Packaging User Guide
# <https://python-packaging-user-guide.readthedocs.org/en/latest/tutorial.html#id30>`_
def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()
    
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
        version_file, re.M)
    if version_match:
        return version_match.group(1)
    
    raise RuntimeError("Unable to find the version string.")


setuptools.setup(
    name='gorilla',
    version=find_version('gorilla', '__init__.py'),
    description='Convenient approach to monkey patching.',
    keywords='gorilla monkey patch',
    license='MIT',
    url='https://github.com/christophercrouzet/gorilla',
    author='Christopher Crouzet',
    author_email='christopher.crouzet@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    packages=setuptools.find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False
)
