#!/usr/bin/env python
import re
import sys

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
    def single_tag(self):
        return self.kind in ['br', 'img', 'b']

    @property
    def value(self):
        return self._value

    @property
    def kind(self):
        m = HtmlTag.TAG_KIND_PATTERN.match(self.value)
        return m.group(1).lower()

    @property
    def open_tag(self):
        return not self.close_tag

    @property
    def close_tag(self):
        return HtmlTag.END_TAG_PATTERN.match(self.value)

    @property
    def is_comment(self):
        return self.value.startswith('<--') or self.value.endswith('-->')

    def match(self, other):
        return self.kind == other.kind and (self.open_tag != other.open_tag)


class Result:
    def __init__(self, status, reason, detail):
        self._status = status
        self._reason = reason
        self._detail = detail

    @property
    def status(self):
        return self._status

    @property
    def reason(self):
        return self._reason

    @property
    def detail(self):
        return self._detail

    @staticmethod
    def ok():
        return Result(True, "", "")

    @staticmethod
    def not_found_close_tag():
        return Result(False, "NOT_FOUND_CLOSE_TAG", "")

    @staticmethod
    def not_found_open_tag():
        return Result(False, "NOT_FOUND_OPEN_TAG", "")

    @staticmethod
    def unmatch_tag(open, close):
        return Result(False, "FOUND_UN_MATCH_TAG", "open:" + open.value + " close:" + close.value)


def valid(document):
    stack = []
    ite = HtmlTagIterator(document)
    for tag in ite:
        if tag.is_comment or tag.single_tag:
            pass
        elif tag.open_tag:
            stack.append(tag)
        else:
            if not stack:
                return Result.not_found_open_tag()

            latest = stack.pop()
            if not tag.match(latest):
                return Result.unmatch_tag(latest, tag)

    if not stack:
       return Result.ok()
    else: 
       return Result.not_found_close_tag()

if __name__ == "__main__":
    document = sys.argv[1]
    result = valid(document)
    print result.status
    print result.reason
    print result.detail
