# encoding=utf-8


from nltk import NaiveBayesClassifier

from helpers import getHamContent


def getAccuracy():
    classifier = NaiveBayesClassifier()
