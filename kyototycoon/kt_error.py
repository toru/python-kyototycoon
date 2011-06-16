#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.

class KyotoTycoonError:
    SUCCESS  = 0
    NOIMPL   = 1
    INVALID  = 2
    LOGIC    = 3
    INTERNAL = 4
    NETWORK  = 5
    EMISC    = 255

    ErrorNameDict = {
        SUCCESS: "SUCCESS",
        NOIMPL: "UNIMPLEMENTED",
        INVALID: "INVALID",
        LOGIC: "LOGIC",
        INTERNAL: "INTERNAL",
        NETWORK: "NETWORK",
        EMISC: "EMISC",
    }

    ErrorMessageDict = {
        SUCCESS: "Operation Successful",
        NOIMPL: "Unimplemented Operation",
        INVALID: "Invalid Operation",
        LOGIC: "Logic Error",
        INTERNAL: "Internal Error",
        NETWORK: "Network Error",
        EMISC: "Miscellenious Error",
    }

    def __init__(self):
        self.error_code = self.SUCCESS
        self.error_name = self.ErrorNameDict[self.SUCCESS]
        self.error_message = self.ErrorMessageDict[self.SUCCESS]

    def code(self):
        return self.error_code

    def name(self):
        return self.error_name

    def message(self):
        return self.error_message
