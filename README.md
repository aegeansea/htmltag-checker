# htmltag-checker

simple html tag checker written in Python.


# Overview

This library can find  not match tag.

example

```python
document = '<div><a href="#">sample code </a></div>'
result = checker.valid(document)
result.status #True
```
found not match tag.

```python
document = '<div><a href="#">not found close tag!</div>'
result = checker.valid(document)
result.status #False
result.reason #FOUND_UN_MATCH_TAG
```

# License

Apache License, Version 2.0 

http://www.apache.org/licenses/LICENSE-2.0.html
