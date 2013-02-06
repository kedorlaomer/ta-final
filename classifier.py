# encoding=utf-8

from nltk import NaiveBayesClassifier
from nltk import classify as nltk_classify

from features import featuresForText
from helpers import splitByRatio, getHamContent


def getBayesAccuracy():

    classifier = NaiveBayesClassifier()
    content = getHamContent()
    featureset = []

    for text in content:
        featureset.append(featuresForText(text))
    trainset, devset = splitByRatio(featureset, 0.9)
    classifier.train(trainset)

    return nltk_classify.accuracy(classifier, devset)


if __name__ == '__main__':
    print getBayesAccuracy()
