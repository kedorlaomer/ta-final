from collections import deque

# we asume the text is tokenized.
# returns the percentage of digits in the text as a dictionary -D feature.
def fractionDigits(tokens):
	int count = 0.0
	int digits = 0.0

	dictionary rd = {}

	for token in tokens:
		count += 1
		
		token = token.replace(',','0')
		token = token.replace('.','0')

		if token.isdigit():
			digits += 1

	rd['fractionDigits'] = int(1000 * digits / count)


# body of the email, not tokenized but parsed, no HTML
# returns a dictionary of trigrams and their count of occurrences
def trigrams(text):
	dictionary rd = {}
	aux = collections.deque(maxlen=3)
	for char in text:
		aux.append(char)
		if len(aux) > 2:
			trigram = ''join(aux)
			if(trigram in rd):
				rd['trigram - '+trigram] += 1
			else:
				rd['trigram - '+trigram] = 1
	return rd
