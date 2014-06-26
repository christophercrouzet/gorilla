import difflib
import pprint
import sys
import unittest

from gorilla.extension import Extension


if sys.version_info < (2, 7):
    def safe_repr(object, short=False):
        max_length = 80
        try:
            result = repr(object)
        except Exception:
            import __builtin__
            result = __builtin__.object.__repr__(object)
        
        if not short or len(result) < max_length:
            return result
        
        return result[:max_length] + ' [truncated]...'
else:
    safe_repr = unittest.util.safe_repr


DIFF_OMITTED = ("\nThe difference is %s characters long. "
                "Set self.maxDiff to None to see it.")


class GorillaTestCase(unittest.TestCase):
    
    def setup(self):
        pass
    
    def teardown(self):
        pass
    
    def assert_equal(self, first, second, message=None):
        return self.assertEqual(first, second, msg=message)
    
    def assert_not_equal(self, first, second, message=None):
        return self.assertNotEqual(first, second, msg=message)
    
    def assert_true(self, expression, message=None):
        return self.assertTrue(expression, msg=message)
    
    def assert_false(self, expression, message=None):
        return self.assertFalse(expression, msg=message)
    
    def assert_is(self, expression_1, expression_2, message=None):
        return self.assertIs(expression_1, expression_2, msg=message)
    
    def assert_is_not(self, expression_1, expression_2, message=None):
        return self.assertIsNot(expression_1, expression_2, msg=message)
    
    def assert_is_none(self, object, message=None):
        return self.assertIsNone(object, msg=message)
    
    def assert_is_not_none(self, object, message=None):
        return self.assertIsNotNone(object, msg=message)
    
    def assert_in(self, member, container, message=None):
        return self.assertIn(member, container, msg=message)
    
    def assert_not_in(self, member, container, message=None):
        return self.assertNotIn(member, container, msg=message)
    
    def assert_isinstance(self, object, cls, message=None):
        return self.assertIsInstance(object, cls, msg=message)
    
    def assert_not_isinstance(self, object, cls, message=None):
        return self.assertNotIsInstance(object, cls, msg=message)
    
    def assert_list_equal(self, list_1, list_2, message=None):
        return self.assertListEqual(list_1, list_2, msg=message)
    
    def assert_count_equal(self, first, second, message=None):
        return self.assertCountEqual(first, second, msg=message)
    
    def assert_extension_equal(self, extension_1, extension_2, message=None):
        return self.assertExtensionEqual(extension_1, exception_2, msg=message)
    
    def assert_raises(self, exception_class, callable=None, *args, **kwargs):
        return self.assertRaises(exception_class, callable, *args, **kwargs)
    
    def setUp(self):
        self.setup()
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.teardown()
    
    def assertExtensionEqual(self, extension1, extension2, msg=None):
        self.assertIsInstance(extension1, Extension,
                               'First argument is not an extension')
        self.assertIsInstance(extension2, Extension,
                               'Second argument is not an extension')
        if extension1.name != extension2.name:
            standardMsg = 'Name differs: %s != %s' % (
                extension1.name, extension2.name)
        elif extension1.original != extension2.original:
            standardMsg = 'Original object differs: %s != %s' % (
                extension1.original, extension2.original)
        elif extension1.__dict__ != extension2.__dict__:
            standardMsg = '__dict__ attribute differs: %s != %s' % (
                extension1.__dict__, extension2.__dict__)
        else:
            return
        
        msg = self._formatMessage(msg, standardMsg)
        raise self.failureException(msg)
    
    # Reimplement the methods added in Python 2.7 for Python 2.6.
    if sys.version_info < (2, 7):
        longMessage = True
        maxDiff = 80*8
        _diffThreshold = 2**16
        
        def __init__(self,*args, **kwargs):
            super(GorillaTestCase, self).__init__(*args, **kwargs)
            self._type_equality_funcs = {}
            self.addTypeEqualityFunc(dict, 'assertDictEqual')
            self.addTypeEqualityFunc(list, 'assertListEqual')
            self.addTypeEqualityFunc(tuple, 'assertTupleEqual')
            self.addTypeEqualityFunc(set, 'assertSetEqual')
            self.addTypeEqualityFunc(frozenset, 'assertSetEqual')
            self.addTypeEqualityFunc(str, 'assertMultiLineEqual')
            self.addTypeEqualityFunc(Extension, 'assertExtensionEqual')
        
        def addTypeEqualityFunc(self, typeobj, function):
            self._type_equality_funcs[typeobj] = function
        
        def assertEqual(self, first, second, msg=None):
            assertion_func = self._getAssertEqualityFunc(first, second)
            assertion_func(first, second, msg=msg)
        
        def assertNotEqual(self, first, second, msg=None):
            if not first != second:
                msg = self._formatMessage(msg, '%s == %s' % (
                    safe_repr(first), safe_repr(second)))
        
        def assertIs(self, expr1, expr2, msg=None):
            if expr1 is not expr2:
                standardMsg = '%s is not %s' % (safe_repr(expr1),
                                                safe_repr(expr2))
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertIsNot(self, expr1, expr2, msg=None):
            if expr1 is expr2:
                standardMsg = 'unexpectedly identical: %s' % (
                    safe_repr(expr1),)
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertIsNone(self, obj, msg=None):
            if obj is not None:
                standardMsg = '%s is not None' % (safe_repr(obj),)
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertIsNotNone(self, obj, msg=None):
            if obj is None:
                standardMsg = 'unexpectedly None'
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertIn(self, member, container, msg=None):
            if member not in container:
                standardMsg = '%s not found in %s' % (safe_repr(member),
                                                      safe_repr(container))
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertNotIn(self, member, container, msg=None):
            if member in container:
                standardMsg = '%s unexpectedly found in %s' % (
                    safe_repr(member), safe_repr(container))
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertIsInstance(self, obj, cls, msg=None):
            if not isinstance(obj, cls):
                standardMsg = '%s is not an instance of %r' % (safe_repr(obj),
                                                               cls)
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertNotIsInstance(self, obj, cls, msg=None):
            if isinstance(obj, cls):
                standardMsg = '%s is an instance of %r' % (safe_repr(obj), cls)
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertDictEqual(self, d1, d2, msg=None):
            self.assertIsInstance(d1, dict,
                'First argument is not a dictionary')
            self.assertIsInstance(d2, dict,
                'Second argument is not a dictionary')
            
            if d1 != d2:
                standardMsg = '%s != %s' % (safe_repr(d1, True),
                                            safe_repr(d2, True))
                diff = ('\n' + '\n'.join(difflib.ndiff(
                               pprint.pformat(d1).splitlines(),
                               pprint.pformat(d2).splitlines())))
                standardMsg = self._truncateMessage(standardMsg, diff)
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertListEqual(self, list1, list2, msg=None):
            self.assertSequenceEqual(list1, list2, msg, seq_type=list)
        
        def assertTupleEqual(self, tuple1, tuple2, msg=None):
            self.assertSequenceEqual(tuple1, tuple2, msg, seq_type=tuple)
        
        def assertSetEqual(self, set1, set2, msg=None):
            try:
                difference1 = set1.difference(set2)
            except TypeError as e:
                self.fail(
                    'invalid type when attempting set difference: %s' % e)
            except AttributeError as e:
                self.fail(
                    'first argument does not support set difference: %s' % e)
            
            try:
                difference2 = set2.difference(set1)
            except TypeError as e:
                self.fail(
                    'invalid type when attempting set difference: %s' % e)
            except AttributeError as e:
                self.fail(
                    'second argument does not support set difference: %s' % e)
            
            if not (difference1 or difference2):
                return
            
            lines = []
            if difference1:
                lines.append('Items in the first set but not the second:')
                for item in difference1:
                    lines.append(repr(item))
            if difference2:
                lines.append('Items in the second set but not the first:')
                for item in difference2:
                    lines.append(repr(item))
            
            standardMsg = '\n'.join(lines)
            self.fail(self._formatMessage(msg, standardMsg))
        
        def assertMultiLineEqual(self, first, second, msg=None):
            self.assertIsInstance(first, str,
                                  'First argument is not a string')
            self.assertIsInstance(second, str,
                                  'Second argument is not a string')
            
            if first != second:
                # don't use difflib if the strings are too long
                if (len(first) > self._diffThreshold or
                    len(second) > self._diffThreshold):
                    self._baseAssertEqual(first, second, msg)
                firstlines = first.splitlines(keepends=True)
                secondlines = second.splitlines(keepends=True)
                if len(firstlines) == 1 and first.strip('\r\n') == first:
                    firstlines = [first + '\n']
                    secondlines = [second + '\n']
                standardMsg = '%s != %s' % (safe_repr(first, True),
                                            safe_repr(second, True))
                diff = '\n' + ''.join(difflib.ndiff(firstlines, secondlines))
                standardMsg = self._truncateMessage(standardMsg, diff)
                self.fail(self._formatMessage(msg, standardMsg))
        
        def assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None):
            if seq_type is not None:
                seq_type_name = seq_type.__name__
                if not isinstance(seq1, seq_type):
                    raise self.failureException(
                        'First sequence is not a %s: %s' % (
                            seq_type_name, safe_repr(seq1)))
                if not isinstance(seq2, seq_type):
                    raise self.failureException(
                        'Second sequence is not a %s: %s' % (
                            seq_type_name, safe_repr(seq2)))
            else:
                seq_type_name = "sequence"
            
            differing = None
            try:
                len1 = len(seq1)
            except (TypeError, NotImplementedError):
                differing = 'First %s has no length.    Non-sequence?' % (
                        seq_type_name)
            
            if differing is None:
                try:
                    len2 = len(seq2)
                except (TypeError, NotImplementedError):
                    differing = 'Second %s has no length.    Non-sequence?' % (
                            seq_type_name)
            
            if differing is None:
                if seq1 == seq2:
                    return
                
                seq1_repr = safe_repr(seq1)
                seq2_repr = safe_repr(seq2)
                if len(seq1_repr) > 30:
                    seq1_repr = seq1_repr[:30] + '...'
                if len(seq2_repr) > 30:
                    seq2_repr = seq2_repr[:30] + '...'
                elements = (seq_type_name.capitalize(), seq1_repr, seq2_repr)
                differing = '%ss differ: %s != %s\n' % elements
                
                for i in range(min(len1, len2)):
                    try:
                        item1 = seq1[i]
                    except (TypeError, IndexError, NotImplementedError):
                        differing += (
                            '\nUnable to index element %d of first %s\n' % (
                                i, seq_type_name))
                        break
                    
                    try:
                        item2 = seq2[i]
                    except (TypeError, IndexError, NotImplementedError):
                        differing += (
                            '\nUnable to index element %d of second %s\n' % (
                                i, seq_type_name))
                        break
                    
                    if item1 != item2:
                        differing += (
                            '\nFirst differing element %d:\n%s\n%s\n' % (
                                i, item1, item2))
                        break
                else:
                    if (len1 == len2 and seq_type is None and
                        type(seq1) != type(seq2)):
                        # The sequences are the same, but have differing types.
                        return
                
                if len1 > len2:
                    differing += (
                        '\nFirst %s contains %d additional elements.\n' % (
                            seq_type_name, len1 - len2))
                    try:
                        differing += (
                            'First extra element %d:\n%s\n' % (
                                len2, seq1[len2]))
                    except (TypeError, IndexError, NotImplementedError):
                        differing += (
                            'Unable to index element %d of first %s\n' % (
                                len2, seq_type_name))
                elif len1 < len2:
                    differing += (
                        '\nSecond %s contains %d additional elements.\n' % (
                            seq_type_name, len2 - len1))
                    try:
                        differing += (
                            'First extra element %d:\n%s\n' % (
                                len1, seq2[len1]))
                    except (TypeError, IndexError, NotImplementedError):
                        differing += (
                            'Unable to index element %d of second %s\n' % (
                                len1, seq_type_name))
            
            standardMsg = differing
            diffMsg = '\n' + '\n'.join(
                difflib.ndiff(pprint.pformat(seq1).splitlines(),
                              pprint.pformat(seq2).splitlines()))
            
            standardMsg = self._truncateMessage(standardMsg, diffMsg)
            msg = self._formatMessage(msg, standardMsg)
            self.fail(msg)
        
        def _getAssertEqualityFunc(self, first, second):
            if type(first) is type(second):
                asserter = self._type_equality_funcs.get(type(first))
                if asserter is not None:
                    if isinstance(asserter, str):
                        asserter = getattr(self, asserter)
                    return asserter
            
            return self._baseAssertEqual
        
        def _baseAssertEqual(self, first, second, msg=None):
            if not first == second:
                standardMsg = '%s != %s' % (safe_repr(first),
                                            safe_repr(second))
                msg = self._formatMessage(msg, standardMsg)
                raise self.failureException(msg)
        
        def _formatMessage(self, msg, standardMsg):
            if not self.longMessage:
                return msg or standardMsg
            if msg is None:
                return standardMsg
            try:
                # don't switch to '{}' formatting in Python 2.X
                # it changes the way unicode input is handled
                return '%s : %s' % (standardMsg, msg)
            except UnicodeDecodeError:
                return  '%s : %s' % (safe_repr(standardMsg), safe_repr(msg))
        
        def _truncateMessage(self, message, diff):
            max_diff = self.maxDiff
            if max_diff is None or len(diff) <= max_diff:
                return message + diff
            return message + (DIFF_OMITTED % len(diff))
    else:
        def __init__(self,*args, **kwargs):
            super(GorillaTestCase, self).__init__(*args, **kwargs)
            self.addTypeEqualityFunc(Extension, 'assertExtensionEqual')
