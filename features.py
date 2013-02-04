# encoding=utf-8

from nltk import word_tokenize
from collections import deque

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
	for char in text:
		aux.append(char)
		if len(aux) > 2:
			trigram = ''.join(aux)
			if('trigram - '+trigram in rd):
				rd['trigram - '+trigram] += 1
			else:
				rd['trigram - '+trigram] = 1
	return rd
