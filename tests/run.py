#!/usr/bin/env python

import collections
import optparse
import os
import subprocess
import sys
import unittest


def _find_tests(path, selectors=None):
    if selectors is None:
        def filter(test):
            return True
    else:
        def filter(test):
            return any(selector in _get_test_name(test)
                       for selector in selectors)

    out = []
    stack = collections.deque((unittest.TestLoader().discover(path),))
    while stack:
        obj = stack.popleft()
        if isinstance(obj, unittest.TestSuite):
            stack.extend(test for test in obj)
        elif filter(obj):
            out.append(obj)

    return out


def _get_test_name(test):
    return '%s.%s.%s' % (
        test.__class__.__module__, test.__class__.__name__,
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
    root_path = os.path.abspath(os.path.join(here, os.pardir))
    sys.path.insert(0, root_path)

    selectors = args if args else None
    tests = _find_tests(here, selectors)

    if options.split:
        for test in tests:
            name = _get_test_name(test)
            subprocess.call([sys.executable, '-m', 'unittest', '-v', name],
                            env={'PYTHONPATH': ':'.join(sys.path)})
    else:
        suite = unittest.TestLoader().suiteClass(tests)
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    main()
