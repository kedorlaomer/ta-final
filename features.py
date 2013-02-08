# encoding=utf-8

import re
import codecs
import email.parser
from collections import deque
from htmlParser import MyHTMLParser

from nltk import word_tokenize


PROMILLE = 10
SPECIAL_CHARS = "@`!\"#$%&()*:+;[{,<\|-=]}.>^~/?_"
MAIL_PARSER = email.parser.Parser()
HTML_PARSER = MyHTMLParser()
LINK_RE = re.compile(r"""
    (http|ftp|https|mailto):
    \/\/[\w\-_]+(\.[\w\-_]+)+
    ([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?
""", re.X)


def isLink(token):
    return bool(LINK_RE.match(token))


def linkCounter(tokens):
    linkCount = sum(1 for x in tokens if isLink(x))
    rv = linkCount / (len(tokens) or 1)

    return {'links count (prodec)': PROMILLE * int(rv * PROMILLE)}


def citationLineCounter(text):
    citationLineCount = text.count("\n> ")
    rv = float(citationLineCount) / (text.count("\n") or 1)

    return {'citation line count (prodec)': int(PROMILLE * rv)}


# tokenized
def fractionCapitals(tokens):
    total = len(tokens)
    capitals = sum(1 for x in tokens if x.isupper())

    rv = float(capitals) / (total or 1)
    rv = int(PROMILLE * rv)
    return {"capital-only tokens (prodec)": rv}


# not tokenized
def fractionSpecialChars(text):
    rv = {}
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

    count = len(tokens)
    digits = 0

    for token in tokens:

        token = token.replace(',', '0')
        token = token.replace('.', '0')

        if token.isdigit():
            digits += 1

    return {'fractionDigits': int(PROMILLE * digits / (count or 1))}


# body of the email, not tokenized but parsed, no HTML
# returns a dictionary of trigrams and their count of occurrences
def trigrams(text):
    rd = {}
    aux = deque(maxlen=3)
    for char in text.lower():
        aux.append(char)
        if len(aux) > 2:
            trigram = ''.join(aux)
            rd['trigram - ' + trigram] = 1
    return rd


def tokenFeature(tokens):
    rv = {}
    for token in tokens:
        rv["token " + token.lower()] = 1
    return rv


def isHTML(text):
    return "<html>" in text.lower()


# returns title, followed by \n, followed by body of given html
def htmlText(html):
    HTML_PARSER.reset()
    HTML_PARSER.feed(html)
    return HTML_PARSER.title.strip() + "\n" + HTML_PARSER.body.strip()


def htmlFeatures(html):
    rv = {"is html ": 1}
    rv["colored parts "] = min(2, HTML_PARSER.colorCount)
    rv["font'ed parts "] = min(2, HTML_PARSER.fontCount)
    return rv

# functions working on specific parts/formats of a message
TOKEN_FUNCTIONS = [fractionCapitals, fractionDigits, linkCounter, tokenFeature]
TEXT_FUNCTIONS  = [fractionSpecialChars, trigrams]
UNPARSED_FUNCTIONS = [citationLineCounter]
STOP_WORDS      = set()  # read it later

with open("english_stop_words.txt") as f:
    for word in f:
        word = word.strip()
        STOP_WORDS.add(word)

STOP_WORDS = frozenset(STOP_WORDS)


# somehow (??) deal with unicode
def toUni(string):
    if not isinstance(string, unicode):
        return unicode(string, "latin-1", "ignore")
    return string


def featuresForMail(path):
    p = MAIL_PARSER
    with codecs.open(path) as f:
        mail = p.parse(f)
    return featuresForText(mail)


def headerFeatures(mail):
    rv = {}
    rv["has reply-to"] = "Reply-To" in mail
    rv["has in-reply-to"] = "In-Reply-To" in mail

    if "To" in mail and not mail["To"]:
        rv["to-empty"] = True
    if "X-Keywords" in mail and not mail["X-Keywords"]:
        rv["x-keywords-empty"] = True

    contentType = mail["Content-Type"]
    if contentType is not None:
        index = contentType.find(";")
        rv["has content-type"] = contentType if index == -1 else contentType[:index]

    return rv


# text is the subject line of a mail
def subjectFeatures(text):
    d = {}

    if text:
        d.update(tokenFeature(word_tokenize(text)))
        d.update(trigrams(text))
        d.update(fractionCapitals(text))
        d.update(fractionDigits(text))
        d.update(fractionSpecialChars(text))

    rv = {}

    for (key, value) in d.iteritems():
        rv["in subject " + key] = value

    return rv


def featuresForText(mail):
# text of the email
    fullText = ""
    unparsedText = ""
    html = ""
    for part in mail.walk():
        if not part.is_multipart():
            fullText += "\n" + toUni(part.get_payload(decode=True))
            unparsedText += "\n" + toUni(part.get_payload(decode=False))

            if isHTML(fullText):
                html = toUni(fullText)
                fullText = htmlText(html)
                unparsedText = htmlText(toUni(unparsedText))

    rv = {}
    tokens = word_tokenize(fullText)

    # remove stop words
    tokens = filter(lambda token: token not in STOP_WORDS, tokens)
    fullText = " ".join(tokens)

    for function in TEXT_FUNCTIONS:
        data = function(fullText)
        rv.update(data)

    for function in TOKEN_FUNCTIONS:
        data = function(tokens)
        rv.update(data)

    for function in UNPARSED_FUNCTIONS:
        data = function(unparsedText)
        rv.update(data)

    rv.update(headerFeatures(mail))
    rv.update(htmlFeatures(html))
    rv.update(subjectFeatures(mail["Subject"]))

    return rv
