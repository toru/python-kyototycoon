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

KT_PACKER_CUSTOM = 0
KT_PACKER_PICKLE = 1
KT_PACKER_JSON   = 2
KT_PACKER_STRING = 3

class ProtocolHandler:
    def __init__(self, pickle_protocol=2):
        self.error_obj = kt_error.KyotoTycoonError()
        self.pickle_protocol = pickle_protocol
        self.pack = self._pickle_packer
        self.unpack = self._pickle_unpacker
        self.pack_type = KT_PACKER_PICKLE

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

    def get(self, key, db=None):
        if key is None:
            return False

        path = key
        if db:
            path = '/%s/%s' % (db, key)
        path = urllib.quote(path.encode('UTF-8'))

        self.conn.request('GET', path)
        rv = self.conn.getresponse()
        body = rv.read()

        if rv.status != 200:
            return None

        return self.unpack(body)

    def set_bulk(self, kv_dict, expire, atomic, db):
        if not isinstance(kv_dict, dict):
            return False 

        if len(kv_dict) < 1:
            return False

        path = '/rpc/set_bulk'
        if db:
            db = urllib.quote(db)
            path += '?DB=' + db

        request_body = ''

        if atomic:
            request_body = 'atomic\t\n'

        for k, v in kv_dict.items():
            k = urllib.quote(k)
            v = urllib.quote(self.pack(v))
            request_body += '_' + k + '\t' + v + '\n'

        self.conn.request('POST', path, body=request_body,
                          headers=KT_HTTP_HEADER)

        res = self.conn.getresponse()
        body = res.read()

        if res.status != 200:
            return False 

        return int(self._tsv_to_dict(body)['num'])

    def remove_bulk(self, keys, atomic, db):
        if not isinstance(keys, list):
            return 0

        if len(keys) < 1:
            return 0

        path = '/rpc/remove_bulk'
        if db:
            db = urllib.quote(db)
            path += '?DB=' + db

        request_body = ''

        if atomic:
            request_body = 'atomic\t\n'

        for key in keys:
            request_body += '_' + urllib.quote(key) + '\t\n'

        self.conn.request('POST', path, body=request_body,
                          headers=KT_HTTP_HEADER)

        res = self.conn.getresponse()
        body = res.read()

        if res.status != 200:
            return False

        return int(self._tsv_to_dict(body)['num'])

    def get_bulk(self, keys, atomic, db):
        if not isinstance(keys, list):
            return None

        if len(keys) < 1:
            return {} 

        path = '/rpc/get_bulk'
        if db:
            db = urllib.quote(db)
            path += '?DB=' + db

        request_body = ''

        if atomic:
            request_body = 'atomic\t\n'

        for key in keys:
            request_body += '_' + urllib.quote(key) + '\t\n'

        self.conn.request('POST', path, body=request_body,
                          headers=KT_HTTP_HEADER)

        res = self.conn.getresponse()
        body = res.read()

        if res.status != 200:
            return None

        rv = {}
        res_dict = self._tsv_to_dict(body)
        n = res_dict.pop('num')

        if n == 0:
            return None

        for k, v in res_dict.items():
            if v is not None:
                rv[urllib.unquote(k[1:])] = self.unpack(urllib.unquote(v))
        return rv

    def get_int(self, key, db=None):
        if key is None:
            return False

        path = key
        if db:
            path = '/%s/%s' % (db, key)
        path = urllib.quote(path.encode('UTF-8'))

        self.conn.request('GET', path)
        rv = self.conn.getresponse()
        buf = rv.read()

        if rv.status != 200:
            return None

        return struct.unpack('>q', buf)[0]

    def vacuum(self, db):
        path = '/rpc/vacuum'

        if db:
            db = urllib.quote(db)
            path += '?DB=' + db

        self.conn.request('GET', path)
        res = self.conn.getresponse()
        body = res.read()
        return res.status == 200

    def match_prefix(self, prefix, max, db):
        if prefix is None:
            return False

        rv = []
        request_dict = {}
        request_dict['prefix'] = prefix

        if max:
            request_dict['max'] = max
        if db:
            request_dict['DB'] = db

        request_body = self._dict_to_tsv(request_dict)
        self.conn.request('POST', '/rpc/match_prefix',
                          body=request_body, headers=KT_HTTP_HEADER)

        res = self.conn.getresponse()
        body = res.read()

        if res.status != 200:
            return False

        res_dict = self._tsv_to_dict(body)
        n = res_dict.pop('num')

        if n == 0:
            return None

        for k in res_dict.keys():
            rv.append(k[1:])

        return rv

    def set(self, key, value, expire, db=None):
        if key is None:
            return False

        if db:
            key = '/%s/%s' % (db, key)
        key = urllib.quote(key.encode('UTF-8'))
        value = self.pack(value)
        return self._rest_put('set', key, value, expire) == 201

    def add(self, key, value, expire, db):
        if key is None:
            return False

        if db:
            key = '/%s/%s' % (db, key)
        key = urllib.quote(key.encode('UTF-8'))
        value = self.pack(value)
        return self._rest_put('add', key, value, expire) == 201

    def cas(self, key, old_val, new_val, expire, db):
        if key is None:
            return False

        path = '/rpc/cas'
        if db:
            path += '?DB=' + db

        request_dict = { 'key': key }

        if old_val:
            request_dict['oval'] = urllib.quote(self.pack(old_val))
        if new_val:
            request_dict['nval'] = urllib.quote(self.pack(new_val))
        if expire:
            request_dict['xt'] = expire

        request_body = self._dict_to_tsv(request_dict)

        self.conn.request('POST', path, body=request_body,
                          headers=KT_HTTP_HEADER)

        res = self.conn.getresponse()
        body = res.read()
        return res.status == 200

    def remove(self, key, db):
        if key is None:
            return False

        if db:
            key = '/%s/%s' % (db, key)

        key = urllib.quote(key.encode('UTF-8'))
        self.conn.request('DELETE', key)
        rv = self.conn.getresponse()
        body = rv.read()
        return rv.status == 204

    def replace(self, key, value, expire, db):
        if key is None:
            return False

        if db:
            key = '/%s/%s' % (db, key)
        key = urllib.quote(key.encode('UTF-8'))
        value = self.pack(value)
        return self._rest_put('replace', key, value, expire) == 201

    def append(self, key, value, expire, db):
        if key is None:
            return False
        elif not isinstance(value, str):
            return False

        # Only handle Pickle for now.
        if self.pack_type == KT_PACKER_PICKLE:
            data = self.get(key)
            if data is None:
                data = value
            else:
                data = data + value
            return self.set(key, data, expire, db)

        return False

    def increment(self, key, delta, expire, db):
        if key is None:
            return False

        path = '/rpc/increment'
        if db:
            path += '?DB=' + db

        delta = int(delta)
        request_body = 'key\t%s\nnum\t%d\n' % (key, delta)
        self.conn.request('POST', path, body=request_body,
                          headers=KT_HTTP_HEADER)

        res = self.conn.getresponse()
        body = res.read()

        if res.status != 200:
            return None

        return int(self._tsv_to_dict(body)['num'])

    def increment_double(self, key, delta, expire, db):
        if key is None:
            return False

        path = '/rpc/increment_double'
        if db:
            path += '?DB=' + db

        delta = float(delta)
        request_body = 'key\t%s\nnum\t%f\n' % (key, delta)
        self.conn.request('POST', path, body=request_body,
                          headers=KT_HTTP_HEADER)

        res = self.conn.getresponse()
        body = res.read()

        if res.status != 200:
            return None

        return float(self._tsv_to_dict(body)['num'])

    def report(self):
        self.conn.request('GET', '/rpc/report')
        res = self.conn.getresponse()
        body = res.read()
        if res.status != 200:
            return None
        return self._tsv_to_dict(body)

    def status(self, db=None):
        url = '/rpc/status'

        if db:
            db = urllib.quote(db)
            url += '?DB=' + db

        self.conn.request('GET', url)
        res = self.conn.getresponse()
        body = res.read()
        if res.status != 200:
            return None
        return self._tsv_to_dict(body)

    def clear(self, db=None):
        url = '/rpc/clear'

        if db:
            db = urllib.quote(db)
            url += '?DB=' + db

        self.conn.request('GET', url)
        res = self.conn.getresponse()
        body = res.read()
        return True if res.status == 200 else False

    def count(self, db=None):
        dict = self.status(db)
        return int(dict['count'])

    def size(self, db=None):
        dict = self.status(db)
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

    def _rest_put(self, operation, key, value, expire):
        headers = { 'X-Kt-Mode' : operation }
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
