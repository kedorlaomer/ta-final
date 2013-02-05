from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.inBody = False
		self.inTitle = False
		self.body = ''
		self.title = ''
		self.colorCount = 0
		self.fontCount = 0


	def handle_starttag(self, tag, attrs):
		tag = tag.lower()
		if tag == 'body':
			# print "in body!!"
			self.inBody = True
		elif tag == 'title':
			# print "in title!!"
			self.inTitle = True
		elif tag == 'color':
			self.colorCount += 1
		elif tag == 'font':
			self.fontCount += 1

	def handle_endtag(self, tag):
		tag = tag.lower()
		if tag == 'body':
			# print "out body"
			self.inBody = False
		elif tag == 'title':
			# print "out title"
			self.inTitle = False

	def handle_data(self, data):
		if self.inTitle:
			self.title += ' '.join(data.split())
			# print "set title"
		if self.inBody:
			# print ' '.join(data.split())
			self.body += (' '+' '.join(data.split()))
			# print "set body"
			# print self.__dict__
			# print self.body







