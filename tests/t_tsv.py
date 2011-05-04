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

    def test_tsv_rpc(self):
        key = 'tabbed\tkey'
        value = 'tabs\tin\tvalue'

        self.assertTrue(self.kt_handle.clear())
        self.assertEqual(self.kt_handle.increment(key, 1024), 1024)


if __name__ == '__main__':
    unittest.main()
