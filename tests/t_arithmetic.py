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

    def test_increment(self):
        self.assertTrue(self.kt_handle.clear())

        key = 'incrkey'
        self.assertEqual(self.kt_handle.increment(key, 10), 10)
        self.assertEqual(self.kt_handle.increment(key, 10), 20)
        self.assertEqual(self.kt_handle.increment(key, 10), 30)
        self.assertEqual(self.kt_handle.increment(key, 10), 40)
        self.assertEqual(self.kt_handle.increment(key, 10), 50)

        # Incrementing against a non numeric value. Must fail.
        self.assertTrue(self.kt_handle.set(key, 'foo'))
        self.assertEqual(self.kt_handle.increment(key, 10), None)
        self.assertEqual(self.kt_handle.increment(key, 10), None)

if __name__ == '__main__':
    unittest.main()
