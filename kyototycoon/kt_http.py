#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.

import httplib
import urllib
import time

class ProtocolHandler:
    def __init__(self):
        pass

    def open(self, host, port, timeout):
        try:
            self.conn = httplib.HTTPConnection(host, port, timeout)
        except Exception, e:
            raise e
        return True

    def close(self):
        try:
            self.conn.close()
        except Exception, e:
            raise e
        return True

    def get(self, key):
        key = key.encode('UTF-8')
        key = urllib.quote(key)
        self.conn.request('GET', key)
        rv = self.conn.getresponse()
        body = rv.read()
        return body if rv.status == 200 else None

    def set(self, key, value, expire):
        headers = {}

        if expire != None:
            expire = int(time.time()) + expire;
            headers["X-Kt-Xt"] = str(expire)

        key = key.encode('UTF-8')
        key = urllib.quote(key)
        self.conn.request('PUT', key, value, headers)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status == 201;

    def add(self, key, value, expire):
        headers = {}
        headers['X-Kt-Mode'] = 'add'

        if expire != None:
            expire = int(time.time()) + expire;
            headers["X-Kt-Xt"] = str(expire)
        
        key = key.encode('UTF-8')
        key = urllib.quote(key)
        self.conn.request('PUT', key, value, headers)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status == 201;

    def remove(self, key):
        key.encode('UTF-8')
        key = urllib.quote(key)
        self.conn.request('DELETE', key)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status == 204

    def replace(self, key, value, expire):
        headers = {}
        headers['X-Kt-Mode'] = 'replace'

        if expire != None:
            expire = int(time.time()) + expire;
            headers["X-Kt-Xt"] = str(expire)
        
        key = key.encode('UTF-8')
        key = urllib.quote(key)
        self.conn.request('PUT', key, value, headers)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status == 201;

    def status(self):
        self.conn.request('GET', '/rpc/status')
        res = self.conn.getresponse()
        body = res.read()
        if res.status != 200:
            return -1
        return self._tsv_to_dict(body)

    def clear(self):
        self.conn.request('GET', '/rpc/clear')
        res = self.conn.getresponse()
        body = res.read()
        return True if res.status == 200 else False

    def count(self):
        dict = self.status()
        return int(dict['count'])

    def size(self):
        dict = self.status()
        return int(dict['size'])

    def _tsv_to_dict(self, tsv_str):
        rv = {}
        for row in tsv_str.split('\n'):
            kv = row.split('\t')
            if len(kv) == 2:
                rv[kv[0]] = kv[1]
        return rv
