# -*- coding: utf-8 -*-

import sys

py_version = sys.version[:3]

is_py2 = (sys.version_info[0] == 2)
is_py26 = sys.version_info[:2] == (2, 6)
is_py3 = (sys.version_info[0] == 3)

if is_py3:
    text_type = str
else:
    text_type = unicode

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote