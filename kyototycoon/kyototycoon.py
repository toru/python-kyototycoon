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

    def set(self, key, value, expire=None, db=None):
        return self.core.set(key, value, expire, db)

    def add(self, key, value, expire=None, db=None):
        return self.core.add(key, value, expire, db)

    def replace(self, key, value, expire=None, db=None):
        return self.core.replace(key, value, expire, db)

    def append(self, key, value, expire=None, db=None):
        return self.core.append(key, value, expire, db)

    def increment(self, key, delta, expire=None, db=None):
        return self.core.increment(key, delta, expire, db)

    def increment_double(self, key, delta, expire=None, db=None):
        return self.core.increment_double(key, delta, expire, db)

    def cas(self, key, old_val=None, new_val=None, expire=None, db=None):
        return self.core.cas(key, old_val, new_val, expire, db)

    def remove(self, key, db=None):
        return self.core.remove(key, db)

    def get(self, key, db=None):
        return self.core.get(key, db)

    def get_int(self, key, db=None):
        return self.core.get_int(key, db)

    def set_bulk(self, kv_dict, expire=None, atomic=True, db=None):
        return self.core.set_bulk(kv_dict, expire, atomic, db)

    def remove_bulk(self, keys, atomic=True, db=None):
        return self.core.remove_bulk(keys, atomic, db)

    def get_bulk(self, keys, atomic=True, db=None):
        return self.core.get_bulk(keys, atomic, db)

    def vacuum(self, db=None):
        return self.core.vacuum(db)

    def match_prefix(self, prefix, max=None, db=None):
        return self.core.match_prefix(prefix, max, db)

    def match_regex(self, regex, max=None, db=None):
        return self.core.match_regex(regex, max, db)
