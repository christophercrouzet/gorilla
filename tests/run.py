#!/usr/bin/env python

import argparse
import collections
import os
import sys
import unittest


# Usage's syntax based on docopt.
_USAGE = "%(prog)s [<name>...]"
_DESCRIPTION = (
    "Runs the tests that have their name containing either one of the 'name' "
    "arguments passed. If no 'name' argument is passed, all the tests are run."
)


def _find_tests(path, selectors=None):
    if selectors is None:
        def filter(test):
            return True
    else:
        def filter(test):
            return any(selector in _get_test_full_name(test)
                       for selector in selectors)

    out = []
    loader = unittest.TestLoader()
    if path == '__main__':
        root_test = loader.loadTestsFromModule(sys.modules[path])
    else:
        root_test = loader.discover(path)

    stack = collections.deque((root_test,))
    while stack:
        obj = stack.popleft()
        if isinstance(obj, unittest.TestSuite):
            stack.extend(test for test in obj)
        elif type(obj).__name__ == 'ModuleImportFailure':
            try:
                # This should always throw an ImportError exception.
                getattr(obj, _get_test_name(obj))()
            except ImportError as e:
                sys.exit(e.message.strip())
        elif filter(obj):
            out.append(obj)

    return out


def _get_test_name(test):
    return test._testMethodName


def _get_test_full_name(test):
    return '%s.%s.%s' % (type(test).__module__, type(test).__name__,
                         _get_test_name(test))


def run(start_path, verbosity=2):
    parser = argparse.ArgumentParser(usage=_USAGE, description=_DESCRIPTION)
    parser.add_argument('name', nargs='*',
                        help='partial test names to search')
    args = parser.parse_args()
    selectors = args.name if args.name else None
    tests = _find_tests(start_path, selectors)
    suite = unittest.TestLoader().suiteClass(tests)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)


if __name__ == "__main__":
    run(os.path.abspath(os.path.dirname(__file__)))
