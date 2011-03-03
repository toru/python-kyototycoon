#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.

class KyotoTycoonError:
    SUCCESS  = 0
    NOIMPL   = 1
    IMVALID  = 2
    LOGIC    = 3
    INTERNAL = 4
    NETWORK  = 5
    EMISK    = 15

    def __init__(self):
        self.error_code = self.SUCCESS

    def code(self):
        return self.error_code

    def name(self):
        pass

    def message(self):
        pass
