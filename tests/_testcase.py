import sys
import unittest


_PY2 = sys.version_info[0] == 2


class GorillaTestCase(unittest.TestCase):

    if _PY2:
        assertCountEqual = unittest.TestCase.assertItemsEqual
