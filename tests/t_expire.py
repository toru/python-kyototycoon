#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.

import config
import time
import unittest
from kyototycoon import KyotoTycoon

class UnitTest(unittest.TestCase):
    def setUp(self):
        self.kt_handle = KyotoTycoon()
        self.kt_handle.open()
        self.LARGE_KEY_LEN = 8000

    def test_set_expire(self):
        self.assertTrue(self.kt_handle.clear())

        # Set record to be expired in 2 seconds.
        self.assertTrue(self.kt_handle.set('key', 'value', 2))
        self.assertEqual(self.kt_handle.get('key'), 'value')
        self.assertEqual(self.kt_handle.count(), 1)

        # Must be expired after 3 seconds.
        time.sleep(3)
        self.assertEqual(self.kt_handle.get('key'), None)
        self.assertEqual(self.kt_handle.count(), 0)

    def test_add_expire(self):
        self.assertTrue(self.kt_handle.clear())

        self.assertTrue(self.kt_handle.add('hello', 'world', 2))
        self.assertEqual(self.kt_handle.get('hello'), 'world')

        time.sleep(3)
        self.assertEqual(self.kt_handle.get('hello'), None)

if __name__ == '__main__':
    unittest.main()
