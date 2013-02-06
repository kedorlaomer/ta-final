# encoding=utf-8

import re
from collections import deque
import email.parser

from nltk import word_tokenize


PROMILLE = 10
SPECIAL_CHARS = "@`!\"#$%&´()*:+;[{,<\|-=]}.>^~/?_"
MAIL_PARSER = email.parser.Parser()
LINK_RE = re.compile(r"""
    (http|ftp|https|mailto):
    \/\/[\w\-_]+(\.[\w\-_]+)+
    ([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?
""", re.X)


def isLink(token):
    return bool(LINK_RE.match(token))


def linkCounter(tokens):
    linkCount = len(filter(isLink, tokens))
    return {
        'links count (prodec)':
        PROMILLE * linkCount / len(tokens)
    }


def citationLineCounter(text):
    citationLineCount = text.count("\n>")
    return {
        'citation line count (prodec)':
        citationLineCount * PROMILLE / (text.count("\n") or 1)
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
    return {"capital-only tokens (prodec)": rv}


# not tokenized
def fractionSpecialChars(text):
    rv = {}
    total = len(text)
    PREFIX = "special char "
    for char in SPECIAL_CHARS:
        rv[PREFIX + char] = 0

    for char in text:
        if char in SPECIAL_CHARS:
            rv[PREFIX + char] = 1

    return rv


# we asume the text is tokenized.
# returns the percentage of digits in the text as a dictionary -D feature.
def fractionDigits(tokens):
    count = 0.0
    digits = 0.0

    for token in tokens:
        count += 1
        
        token = token.replace(',','0')
        token = token.replace('.','0')

        if token.isdigit():
            digits += 1

    return {'fractionDigits':int(PROMILLE * digits / count)}


# body of the email, not tokenized but parsed, no HTML
# returns a dictionary of trigrams and their count of occurrences
def trigrams(text):
    rd = {}
    aux = deque(maxlen=3)
    for char in text.lower():
        aux.append(char)
        if len(aux) > 2:
            trigram = ''.join(aux)
            rd['trigram - '+trigram] = 1
    return rd

# adds (overwriting) all keys from new to old
def addToDict(old, new):
    for (key, value) in new.items():
        old[key] = value

# functions working on specific parts/formats of a message
TOKEN_FUNCTIONS = [fractionCapitals, fractionDigits, linkCounter]
TEXT_FUNCTIONS  = [fractionSpecialChars, trigrams]
HTML_FUNCTIONS  = []
UNPARSED_FUNCTIONS = [citationLineCounter]
STOP_WORDS      = set() # read it later

with open("english_stop_words.txt") as f:
    for word in f:
        word = word.strip()
        STOP_WORDS.add(word)

STOP_WORDS = frozenset(STOP_WORDS)

def isHTML(text):
    return "<html>" in text.lower()


def featuresForMail(path):
    p = MAIL_PARSER
    with open(path) as f:
        mail = p.parse(f)
    return featuresForText(mail)


def featuresForText(mail):

    rv = {}

    # text of the email
    fullText = ""
    unparsedText = ""
    for part in mail.walk():
        if not part.is_multipart():  # TODO: handle HTML
            fullText += "\n" + part.get_payload(decode=True)
            unparsedText += "\n" + part.get_payload(decode=False)

    tokens = word_tokenize(fullText)

    # remove stop words
    tokens = filter(lambda token: token not in STOP_WORDS, tokens)
    fullText = " ".join(tokens)

    for function in TEXT_FUNCTIONS:
        data = function(fullText)
        addToDict(rv, data)

    for function in TOKEN_FUNCTIONS:
        data = function(tokens)
        addToDict(rv, data)

    for function in UNPARSED_FUNCTIONS:
        data = function(unparsedText)
        addToDict(rv, data)

    return rv
