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

    def test_set(self):
        self.assertTrue(self.kt_handle.clear())
        self.assertTrue(self.kt_handle.set('key', 'value'))
        self.assertTrue(self.kt_handle.set('k e y', 'v a l u e'))

        self.assertEqual(self.kt_handle.get('key'), 'value')
        self.assertEqual(self.kt_handle.get('k e y'), 'v a l u e')

        self.assertTrue(self.kt_handle.set('\\key', '\\xxx'))
        self.assertEqual(self.kt_handle.get('\\key'), '\\xxx')
        self.assertEqual(self.kt_handle.count(), 3)

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

if __name__ == '__main__':
    unittest.main()
