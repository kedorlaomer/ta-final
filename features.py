# encoding=utf-8

import re
from collections import deque

from nltk import word_tokenize


PROMILLE = 1000
SPECIAL_CHARS = "@`!\"#$%&´()*:+;[{,<\|-=]}.>^~/?_"
LINK_RE = re.compile(r"""
    (http|ftp|https):
    \/\/[\w\-_]+(\.[\w\-_]+)+
    ([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?
""", re.X)


def isLink(token):
    return bool(LINK_RE.match(token))


def linkCounter(tokens):
    linkCount = len(filter(isLink, tokens))
    return {
        'links count (promille)':
        PROMILLE * linkCount / len(tokens)
    }


def citationLineCounter(text):
    citationLineCount = text.count("\n>")
    return {
        'citation line count (promille)':
        citationLineCount * PROMILLE / text.count("\n")
    }


# tokenized
def fractionCapitals(tokens):
    capitals = 0
    for token in tokens:
        if token.isupper():
            capitals += 1
    total = len(tokens)
    rv = float(capitals)/float(total)
    rv = int(PROMILLE*rv)
    return {"capital-only tokens (promille)": rv}


# not tokenized
def fractionSpecialChars(text):
    rv = {}
    total = len(text)
    PREFIX = "special char (promille)"
    for char in SPECIAL_CHARS:
        rv[PREFIX + char] = 0

    for char in text:
        if char in SPECIAL_CHARS:
            rv[PREFIX + char] += 1

    for key in rv.keys():
        rv[key] = int(rv[key]*PROMILLE/total)

    return rv


# we asume the text is tokenized.
# returns the percentage of digits in the text as a dictionary -D feature.
def fractionDigits(tokens):
    count = 0.0
    digits = 0.0

    rd = {}

    for token in tokens:
        count += 1
        
        token = token.replace(',','0')
        token = token.replace('.','0')

        if token.isdigit():
            digits += 1

    rd['fractionDigits'] = int(PROMILLE * digits / count)


# body of the email, not tokenized but parsed, no HTML
# returns a dictionary of trigrams and their count of occurrences
def trigrams(text):
    rd = {}
    aux = collections.deque(maxlen=3)
    for char in text:
        aux.append(char)
        if len(aux) > 2:
            trigram = ''.join(aux)
            if(trigram in rd):
                rd['trigram - '+trigram] += 1
            else:
                rd['trigram - '+trigram] = 1
    return rd
