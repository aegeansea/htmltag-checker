#!/usr/bin/env python
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


class Result:
    def __init__(self, status, reason):
        self._status = status
        self._reason = reason

    @property
    def status(self):
        return self._status

    @property
    def reason(self):
        return self._reason

    @staticmethod
    def ok():
        return Result(True, "")

    @staticmethod
    def not_found_close_tag():
        return Result(False, "NOT_FOUND_CLOSE_TAG")

    @staticmethod
    def not_found_open_tag():
        return Result(False, "NOT_FOUND_OPEN_TAG")

    @staticmethod
    def unmatch_tag():
        return Result(False, "FOUND_UN_MATCH_TAG")


def valid(document):
    stack = []
    ite = HtmlTagIterator(document)
    for tag in ite:
        if tag.open_tag:
            stack.append(tag)
        else:
            if not stack:
                return Result.not_found_open_tag()

            latest = stack.pop()
            if not tag.match(latest):
                return Result.unmatch_tag()

    if not stack:
       return Result.ok()
    else: 
       return Result.not_found_close_tag()

