# encoding=utf-8


from nltk import NaiveBayesClassifier
from nltk import classify as nltk_classify

from features import featuresForText
from helpers import splitByRatio, getHamContent


def getAccuracy():

    classifier = NaiveBayesClassifier()
    content = getHamContent()
    featureset = []

    for text in content:
        featureset.append(featuresForText(text))
    trainset, devset = splitByRatio(featureset, 0.9)
