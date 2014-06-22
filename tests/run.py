#!/usr/bin/env python

import optparse
import os
import subprocess
import sys
import unittest


def module_iterator(directory, package_dotted_path):
    paths = os.listdir(directory)
    for path in paths:
        full_path = os.path.join(directory, path)
        basename, tail = os.path.splitext(path)
        if basename == '__init__':
            dotted_path = package_dotted_path
        elif package_dotted_path:
            dotted_path = "%s.%s" % (package_dotted_path, basename)
        else:
            dotted_path = basename
        
        if os.path.isfile(full_path):
            if tail != '.py':
                continue
            
            __import__(dotted_path)
            module = sys.modules[dotted_path]
            yield module
        elif os.path.isdir(full_path):
            if not os.path.isfile(os.path.join(full_path, '__init__.py')):
                continue
            
            __import__(dotted_path)
            package = sys.modules[dotted_path]
            yield package
            for module in module_iterator(full_path, dotted_path):
                yield module


def test_iterator(test):
    if hasattr(test, '__iter__'):
        for item in iter(test):
            for subitem in test_iterator(item):
                yield subitem
    else:
        yield test


def get_test_name(test):
    return '%s.%s.%s' % (
        test.__class__.__module__,
        test.__class__.__name__,
        test._testMethodName)


def main():
    usage = "usage: %prog [options] [test1..testN]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option(
        '-s', '--split', action='store_true', dest='split',
        help="run each test in a separate subprocess"
    )
    
    (options, args) = parser.parse_args()
    
    here = os.path.abspath(os.path.dirname(__file__))
    root_path = os.path.abspath(os.path.join(here, '..'))
    sys.path.insert(0, root_path)
    
    loader = unittest.TestLoader()
    tests = []
    for module in module_iterator(here, 'tests'):
        module_tests = loader.loadTestsFromModule(module)
        if module_tests.countTestCases():
            if args:
                for test in test_iterator(module_tests):
                    name = get_test_name(test)
                    if any((arg in name for arg in args)):
                        tests.append(test)
            else:
                tests.extend(test_iterator(module_tests))
    
    if options.split:
        for test in tests:
            name = get_test_name(test)
            subprocess.call([sys.executable, '-m', 'unittest', '-v', name],
                            env={'PYTHONPATH': ':'.join(sys.path)})
    else:
        suite = loader.suiteClass(tests)
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    main()
