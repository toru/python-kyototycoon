#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.

import config
import unittest
import kyototycoon.kt_http

class UnitTest(unittest.TestCase):
    def setUp(self):
        self.kt_core = kyototycoon.kt_http.ProtocolHandler()

    def test_packer(self):
        str = 'hello world sir'
        buf = self.kt_core._pack_data(str)
        assert buf != str
        ret = self.kt_core._unpack_data(buf)
        self.assertEqual(str, ret)

        num = 777
        buf = self.kt_core._pack_data(num)
        assert buf != num
        ret = self.kt_core._unpack_data(buf)
        self.assertEqual(type(num), type(ret))
        self.assertEqual(num, ret)

if __name__ == '__main__':
    unittest.main()
