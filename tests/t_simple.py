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
        self.LARGE_KEY = 8000

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

    def test_remove(self):
        self.assertTrue(self.kt_handle.clear())
        self.assertFalse(self.kt_handle.remove('must fail key'))
        self.assertTrue(self.kt_handle.set('deleteable key', 'xxx'))
        self.assertTrue(self.kt_handle.remove('deleteable key'))

    def test_replace(self):
        self.assertTrue(self.kt_handle.clear())

        # Must Fail - Can't replace something that doesn't exist.
        self.assertFalse(self.kt_handle.replace('xxxxxx', 'some value'))

        # Popuate then Replace.
        self.assertTrue(self.kt_handle.set('apple', 'ringo'))
        self.assertTrue(self.kt_handle.replace('apple', 'apfel'))
        self.assertEqual(self.kt_handle.get('apple'), 'apfel')

    def test_append(self):
        self.assertTrue(self.kt_handle.clear())

        # Nothing to Append to. So, create a new record.
        self.assertTrue(self.kt_handle.append('key', 'tail'))
        self.assertEqual(self.kt_handle.get('key'), 'tail')

        # Test append on existing record.
        self.assertTrue(self.kt_handle.set('key', 'abc'))
        self.assertTrue(self.kt_handle.append('key', 'def'))
        self.assertTrue(self.kt_handle.append('key', 'ghi'))
        self.assertEqual(self.kt_handle.get('key'), 'abcdefghi')

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

    def test_large_key(self):
        large_key = 'x' * self.LARGE_KEY 
        self.assertTrue(self.kt_handle.set(large_key, 'value'))
        self.assertEqual(self.kt_handle.get(large_key), 'value')

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
