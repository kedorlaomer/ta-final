# encoding=utf-8

from nltk import word_tokenize
from collections import deque
import email.parser

SPECIAL_CHARS = "@`!\"#$%&´()*:+;[{,<\|-=]}.>^~/?_"
MAIL_PARSER = email.parser.Parser()

# tokenized
def fractionCapitals(tokens):
    capitals = 0
    for token in tokens:
        if token.isupper():
            capitals += 1
    total = len(tokens)
    rv = float(capitals)/float(total)
    rv = int(1000*rv)
    return {"capital-only tokens (promille) ": rv}

# not tokenized
def fractionSpecialChars(text):
    rv = {}
    total = len(text)
    PREFIX = "special char (promille) "
    for char in SPECIAL_CHARS:
        rv[PREFIX + char] = 0

    for char in text:
        if char in SPECIAL_CHARS:
            rv[PREFIX + char] += 1

    for key in rv.keys():
        rv[key] = int(rv[key]*1000/total)

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

	return {'fractionDigits':int(1000 * digits / count)}


# body of the email, not tokenized but parsed, no HTML
# returns a dictionary of trigrams and their count of occurrences
def trigrams(text):
	rd = {}
	aux = deque(maxlen=3)
	for char in text.lower():
		aux.append(char)
		if len(aux) > 2:
			trigram = ''.join(aux)
			if('trigram - '+trigram in rd):
				rd['trigram - '+trigram] += 1
			else:
				rd['trigram - '+trigram] = 1
	return rd

# adds (overwriting) all keys from new to old
def addToDict(old, new):
    for (key, value) in new.items():
        old[key] = value

TOKEN_FUNCTIONS = [fractionCapitals, fractionDigits]
TEXT_FUNCTIONS  = [fractionSpecialChars, trigrams]
HTML_FUNCTIONS  = []
STOP_WORDS      = set() # read it later

with open("english_stop_words.txt") as f:
    for word in f:
        word = word.strip()
        STOP_WORDS.add(word)

STOP_WORDS = frozenset(STOP_WORDS)

def featuresForMail(path):
    p = MAIL_PARSER
    rv = {}
    with open(path) as f:
        mail = p.parse(f)

# text of the email
        fullText = ""
        for part in mail.walk():
            if not part.is_multipart(): # TODO: handle HTML
                fullText += "\n" + part.get_payload(decode=True)

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

        return rv
