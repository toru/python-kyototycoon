#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.

import config
import unittest
from kyototycoon import KyotoTycoon

class UnitTest(unittest.TestCase):
    def setUp(self):
        self.kt_handle = KyotoTycoon()
        self.kt_handle.open()
        self.LARGE_KEY_LEN = 8000

    def test_set(self):
        self.assertTrue(self.kt_handle.clear())
        self.assertTrue(self.kt_handle.set('key', 'value'))
        self.assertTrue(self.kt_handle.set('k e y', 'v a l u e'))
        self.assertTrue(self.kt_handle.set('k\te\ty', 'tabbed'))

        self.assertEqual(self.kt_handle.get('key'), 'value')
        self.assertEqual(self.kt_handle.get('k e y'), 'v a l u e')
        self.assertEqual(self.kt_handle.get('k\te\ty'), 'tabbed')

        self.assertTrue(self.kt_handle.set('\\key', '\\xxx'))
        self.assertEqual(self.kt_handle.get('\\key'), '\\xxx')
        self.assertEqual(self.kt_handle.count(), 4)

        self.assertTrue(self.kt_handle.set('tabbed\tkey', 'tabbled\tvalue'))
        self.assertTrue(self.kt_handle.get('tabbed\tkey'))

        self.assertFalse(self.kt_handle.set(None, 'value'))
        self.assertFalse(self.kt_handle.get(None))

        self.assertTrue(self.kt_handle.set('cb', 1791))
        self.assertEqual(self.kt_handle.get('cb'), '1791')

        self.assertTrue(self.kt_handle.set('cb', 1791.1226))
        self.assertEqual(self.kt_handle.get('cb'), '1791.1226')

    def test_set_int(self):
        self.assertTrue(self.kt_handle.clear())
        self.assertTrue(self.kt_handle.set_int('key', 1984))

        # get() would fail due to the default serializer.
        self.failIf(self.kt_handle.get('key') == 1984)
        # get_int() must succeed.
        self.assertEqual(self.kt_handle.get_int('key'), 1984)
        # this must fail since set_int() only accepts an integer.
        self.assertFalse(self.kt_handle.set_int('key', '1984'))

    def test_remove(self):
        self.assertTrue(self.kt_handle.clear())
        self.assertFalse(self.kt_handle.remove('must fail key'))
        self.assertTrue(self.kt_handle.set('deleteable key', 'xxx'))
        self.assertTrue(self.kt_handle.remove('deleteable key'))
        self.assertFalse(self.kt_handle.remove(None))

    def test_replace(self):
        self.assertTrue(self.kt_handle.clear())

        # Must Fail - Can't replace something that doesn't exist.
        self.assertFalse(self.kt_handle.replace('xxxxxx', 'some value'))

        # Popuate then Replace.
        self.assertTrue(self.kt_handle.set('apple', 'ringo'))
        self.assertTrue(self.kt_handle.replace('apple', 'apfel'))
        self.assertEqual(self.kt_handle.get('apple'), 'apfel')
        self.assertFalse(self.kt_handle.replace(None, 'value'))

        self.assertTrue(self.kt_handle.replace('apple', 212))
        self.assertEqual(self.kt_handle.get('apple'), '212')
        self.assertTrue(self.kt_handle.replace('apple', 121))
        self.assertEqual(self.kt_handle.get('apple'), '121')

    def test_add(self):
        self.assertTrue(self.kt_handle.clear())
        self.assertTrue(self.kt_handle.set('stewie', 'griffin'))

        # Must Fail - Stewie exists
        self.assertFalse(self.kt_handle.add('stewie', 'hopkin'))

        # New records
        self.assertTrue(self.kt_handle.add('peter', 'griffin'))
        self.assertTrue(self.kt_handle.add('lois', 'griffin'))
        self.assertTrue(self.kt_handle.add('seth', 'green'))
        self.assertTrue(self.kt_handle.add('nyc', 'new york city'))
        self.assertFalse(self.kt_handle.add(None, 'value'))

        self.assertTrue(self.kt_handle.add('number', 111))
        self.assertEqual(self.kt_handle.get('number'), '111')

    def test_large_key(self):
        large_key = 'x' * self.LARGE_KEY_LEN
        self.assertTrue(self.kt_handle.set(large_key, 'value'))
        self.assertEqual(self.kt_handle.get(large_key), 'value')

    def test_report(self):
        report = None
        report = self.kt_handle.report()
        assert report is not None

    def test_status(self):
        self.assertTrue(self.kt_handle.clear())
        status = None
        status = self.kt_handle.status()
        assert status is not None

        self.assertTrue(status['count'], 0)
        self.kt_handle.set('red', 'apple')
        self.kt_handle.set('yellow', 'banana')
        self.kt_handle.set('pink', 'peach')
        self.assertTrue(status['count'], 3)

    def test_error(self):
        self.assertTrue(self.kt_handle.clear())
        kt_error = self.kt_handle.error()
        assert kt_error is not None
        self.assertEqual(kt_error.code(), kt_error.SUCCESS)

if __name__ == '__main__':
    unittest.main()
