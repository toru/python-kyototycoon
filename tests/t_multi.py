#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.
#
# Kyoto Tycoon should be started like this:
#   $ ktserver one.kch two.kch three.kch

import config
import time
import unittest
from kyototycoon import KyotoTycoon

DB_1 = 'one.kch'
DB_2 = 'two.kch'
DB_3 = 'three.kch'

class UnitTest(unittest.TestCase):
    def setUp(self):
        self.kt_handle = KyotoTycoon()
        self.kt_handle.open()
        self.LARGE_KEY_LEN = 8000

    def test_status(self):
        status = self.kt_handle.status(DB_1)
        assert status is not None

        status = self.kt_handle.status(DB_2)
        assert status is not None

        status = self.kt_handle.status(DB_3)
        assert status is not None

        status = self.kt_handle.status('non_existent')
        assert status is None

if __name__ == '__main__':
    unittest.main()
