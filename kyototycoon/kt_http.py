#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.

import httplib
import urllib
import struct
import time
import kt_error

try:
    import cPickle as pickle
except ImportError:
    import pickle

# Stick with URL encoding for now. Eventually run a benchmark
# to evaluate what the most approariate encoding algorithm is.
KT_HTTP_HEADER = {
  'Content-Type' : 'text/tab-separated-values; colenc=U',
}

class ProtocolHandler:
    def __init__(self, pickle_protocol=2):
        self.error_obj = kt_error.KyotoTycoonError()
        self.pickle_protocol = pickle_protocol

    def error(self):
        return self.error_obj

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

    def echo(self):
        self.conn.request('POST', '/rpc/echo')
        res = self.conn.getresponse()
        body = res.read()
        return True if res.status == 200 else False

    def get(self, key):
        if key is None: return False
        key = urllib.quote(key.encode('UTF-8'))
        self.conn.request('GET', key)
        rv = self.conn.getresponse()
        body = rv.read()
        return body if rv.status == 200 else None

    def get_int(self, key):
        if key is None: return False
        key = urllib.quote(key.encode('UTF-8'))
        self.conn.request('GET', key)
        rv = self.conn.getresponse()
        buf = rv.read()

        if rv.status != 200:
            return None

        return struct.unpack('>q', buf)[0]

    def set(self, key, value, expire):
        if key is None:
            return False
        if not isinstance(value, str):
            value = str(value)

        key = urllib.quote(key.encode('UTF-8'))
        value = value.encode('UTF-8')
        return self._rest_put(key, value, expire) == 201

    def set_int(self, key, value, expire):
        if key is None:
            return False
        if not isinstance(value, int):
            return False

        key = urllib.quote(key.encode('UTF-8'))
        value = struct.pack('>q', value)
        return self._rest_put(key, value, expire) == 201

    def add(self, key, value, expire):
        if key is None: return False

        headers = { 'X-Kt-Mode' : 'add' }
        if expire != None:
            expire = int(time.time()) + expire;
            headers["X-Kt-Xt"] = str(expire)

        if not isinstance(value, str):
            value = str(value)
        
        key = urllib.quote(key.encode('UTF-8'))
        value = value.encode('UTF-8')

        self.conn.request('PUT', key, value, headers)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status == 201;

    def remove(self, key):
        if key is None: return False

        key = urllib.quote(key.encode('UTF-8'))
        self.conn.request('DELETE', key)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status == 204

    def replace(self, key, value, expire):
        if key is None: return False

        headers = { 'X-Kt-Mode' : 'replace' }
        if expire != None:
            expire = int(time.time()) + expire;
            headers["X-Kt-Xt"] = str(expire)

        if not isinstance(value, str):
            value = str(value)
        
        key = urllib.quote(key.encode('UTF-8'))
        value = value.encode('UTF-8')

        self.conn.request('PUT', key, value, headers)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status == 201

    def increment(self, key, delta, expire):
        if key is None: return False

        key = urllib.quote(key.encode('UTF-8'))
        delta = int(delta)

        request_body = 'key\t%s\nnum\t%d\n' % (key, delta)
        self.conn.request('POST', '/rpc/increment', body=request_body,
                          headers=KT_HTTP_HEADER)

        res = self.conn.getresponse()
        body = res.read()

        if res.status != 200:
            return None

        return int(self._tsv_to_dict(body)['num'])

    def report(self):
        self.conn.request('GET', '/rpc/report')
        res = self.conn.getresponse()
        body = res.read()
        if res.status != 200:
            return None
        return self._tsv_to_dict(body)
        
    def status(self):
        self.conn.request('GET', '/rpc/status')
        res = self.conn.getresponse()
        body = res.read()
        if res.status != 200:
            return None
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

    def _dict_to_tsv(self, dict):
        return '\n'.join(k + '\t' + str(v) for (k, v) in dict.items())

    def _tsv_to_dict(self, tsv_str):
        rv = {}
        for row in tsv_str.split('\n'):
            kv = row.split('\t')
            if len(kv) == 2:
                rv[kv[0]] = kv[1]
        return rv

    def _rest_put(self, key, value, expire):
        headers = {}
        if expire != None:
            expire = int(time.time()) + expire;
            headers["X-Kt-Xt"] = str(expire)

        self.conn.request('PUT', key, value, headers)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status

    def _pickle_packer(self, data):
        return pickle.dumps(data, self.pickle_protocol)

    def _pickle_unpacker(self, data):
        return pickle.loads(data)
