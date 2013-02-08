# encoding=utf-8

import sys
from random import shuffle

from nltk import NaiveBayesClassifier
from nltk import classify as nltk_classify

from features import featuresForText
from helpers import (
    getHamContent, getSpamContent, getDirContent, iterDirContent,
    saveClassifier, loadClassifier, splitByRatio,
)


CLASSIFIER_PATH = './classifier.data'
SPAM, NOSPAM = (True, False)
S_SPAM, S_NOSPAM = ("SPAM", "NOSPAM")


def getBayesAccuracy(splitRatio=0.9):

    featureset = []

    for text in getSpamContent():
        featureset.append((featuresForText(text), SPAM))
    for text in getHamContent():
        featureset.append((featuresForText(text), NOSPAM))

    shuffle(featureset)
    trainset, devset = splitByRatio(featureset, splitRatio)

    classifier = NaiveBayesClassifier.train(trainset)
    print classifier.show_most_informative_features(10)
    return nltk_classify.accuracy(classifier, devset)


def train(spamDir, hamDir):

    featureset = []

    for text in getDirContent(spamDir):
        featureset.append((featuresForText(text), SPAM))
    for text in getDirContent(hamDir):
        featureset.append((featuresForText(text), NOSPAM))

    shuffle(featureset)
    classifier = NaiveBayesClassifier.train(featureset)
    saveClassifier(classifier, CLASSIFIER_PATH)

    print "Done with learning."


def classify(evalDir, resultFilename):

    classifier = loadClassifier(CLASSIFIER_PATH)
    if not classifier:
        raise Exception("Classifier was not loaded.")
    print "loaded"

    with open(resultFilename, "w") as f:

        for text, filepath in iterDirContent(evalDir, yieldFilepath=True):

            classification = classifier.classify(featuresForText(text))
            f.write("%s\t%s\n" % (
                filepath,
                S_SPAM if classification else S_NOSPAM
            ))

    print "Classified output was saved to file '%s'." % resultFilename
    print "Done with classifying."


def printUsage():
    print """
        Usage:
        python classifier.py learn <spam_dir> <ham_dir>
        python classifier.py classify <directory_name> <result_filename>
    """


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) != 3:
        printUsage()

    elif args[0] == 'learn':
        train(*args[1:])

    elif args[0] == 'classify':
        classify(*args[1:])

    elif args[0] == 'geba':
        print getBayesAccuracy()

    else:
        printUsage()
