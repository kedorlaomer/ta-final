# encoding=utf-8

from nltk import NaiveBayesClassifier
from nltk import classify as nltk_classify

from features import featuresForText
from helpers import splitByRatio, getHamContent, getSpamContent


def getBayesAccuracy():

    featureset = []

    for text in getHamContent():
        featureset.append((featuresForText(text), False))
    for text in getSpamContent():
        featureset.append((featuresForText(text), True))
    trainset, devset = splitByRatio(featureset, 0.9)

    classifier = NaiveBayesClassifier.train(trainset)
    return nltk_classify.accuracy(classifier, devset)


if __name__ == '__main__':
    print getBayesAccuracy()
