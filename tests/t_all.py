#!/usr/bin/env python
#
# Copyright 2011, Toru Maesaka
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.

import os
import re
import unittest

_TEST_MODULE_PATTERN = re.compile(r'^(t_.+)\.py$')

def _run_all_tests():
    module_names = []
    loader = unittest.TestLoader()
    test_path = os.path.join(os.path.split(__file__)[0], '.')

    for filename in os.listdir(test_path):
        match = _TEST_MODULE_PATTERN.search(filename)
        if match:
            module_names.append(match.group(1))

    return loader.loadTestsFromNames(module_names)

if __name__ == '__main__':
    unittest.main(defaultTest='_run_all_tests')
    pass
