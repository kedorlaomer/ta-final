#encode: utf-8
import re


LINK_RE = re.compile(r"""
    (http|ftp|https):
    \/\/[\w\-_]+(\.[\w\-_]+)+
    ([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?
""")


def isLink(token):
    return bool(LINK_RE.match(token))


def linkCounter(cls, tokens):
    linkCount = len(map(isLink, tokens))
    return {'linkCount': linkCount / float(len(tokens))}
