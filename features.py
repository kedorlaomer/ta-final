# encoding=utf-8
from nltk import word_tokenize

SPECIAL_CHARS = "@`!\"#$%&´()*:+;[{,<\|-=]}.>^~/?_"

# tokenized
def fractionCapitals(tokens):
    capitals = 0
    for token in tokens:
        if token.isupper():
            capitals += 1
    total = len(tokens)
    rv = float(capitals)/float(total)
    rv = int(1000*rv)
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
        rv[key] = int(rv[key]*1000/total)

    return rv
