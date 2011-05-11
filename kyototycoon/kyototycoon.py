#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.
#
# Note that python-kyototycoon follows the following interface
# standard: http://fallabs.com/kyototycoon/kyototycoon.idl

import kt_http

KT_DEFAULT_HOST = '127.0.0.1'
KT_DEFAULT_PORT = 1978
KT_DEFAULT_TIMEOUT = 30

class KyotoTycoon:
    def __init__(self, binary=False):
        self.core = kt_http.ProtocolHandler()

    def error(self):
        return self.core.error()

    def open(self, host=KT_DEFAULT_HOST, port=KT_DEFAULT_PORT,
             timeout=KT_DEFAULT_TIMEOUT):
        return self.core.open(host, port, timeout)

    def close(self):
        return self.core.close()

    def report(self):
        return self.core.report()

    def status(self, db=None):
        return self.core.status(db)

    def clear(self, db=None):
        return self.core.clear(db)

    def count(self, db=None):
        return self.core.count(db)

    def size(self, db=None):
        return self.core.size(db)

    def set(self, key, value, expire=None):
        return self.core.set(key, value, expire)

    def set_int(self, key, value, expire=None):
        return self.core.set_int(key, value, expire)

    def add(self, key, value, expire=None):
        return self.core.add(key, value, expire)

    def replace(self, key, value, expire=None):
        return self.core.replace(key, value, expire)

    def append(self, key, value, expire=None):
        return self.core.append(key, value, expire)

    def increment(self, key, delta, expire=None):
        return self.core.increment(key, delta, expire)

    def remove(self, key):
        return self.core.remove(key)

    def get(self, key):
        return self.core.get(key)

    def get_int(self, key):
        return self.core.get_int(key)

    def vacuum(self):
        return self.core.vacuum()
