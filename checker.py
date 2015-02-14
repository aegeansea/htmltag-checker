#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Created:  2015-02-14
#

import re

class HtmlTagIterator:
    def __init__(self, document):
        p = re.compile('<[^>]+>')
        self.iterator = p.finditer(document)

    def __iter__(self):
        return self

    def next(self):
        return HtmlTag(self.iterator.next().group())

class HtmlTag:
    END_TAG_PATTERN = re.compile('<[ ]*/.*')
    TAG_KIND_PATTERN = re.compile('<[ ]*/?[ ]*([a-zA-Z]+).*>')
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def kind(self):
        m = HtmlTag.TAG_KIND_PATTERN.match(self.value)
        return m.group(1)

    @property
    def open_tag(self):
        return not self.close_tag

    @property
    def close_tag(self):
        return HtmlTag.END_TAG_PATTERN.match(self.value)

    def match(self, other):
        return self.kind == other.kind and (self.open_tag != other.open_tag)

