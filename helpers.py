# encoding=utf-8

import os
import cPickle
from random import random

from features import MAIL_PARSER as mp


def iterDirContent(dirpath, yieldFilepath=False):

    try:
        dirlist = os.listdir(dirpath)

        for filepath in dirlist:
            with open(os.path.join(dirpath, filepath), 'r') as f:
                if yieldFilepath:
                    yield mp.parse(f), filepath
                else:
                    yield mp.parse(f)

    except Exception as ex:
        print 'Error occured while reading directory:', ex


def getDirContent(dirpath):
    return list(iterDirContent(dirpath))


def getHamContent():
    return getDirContent('trainingham')


def getSpamContent():
    return getDirContent('trainingspam')


def saveClassifier(classifier, filename):

    with open(filename, 'wb') as f:
        cPickle.dump(classifier, f)
    print "Classifier was successfully dumped to the file '%s'." % (
        filename)


def loadClassifier(filename):
    if not os.path.isfile(filename):
        print "File '%s' don't exists!" % filename
        return None

    with open(filename) as f:
        classifier = cPickle.load(f)
    return classifier


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def splitByRatio(texts, ratio):

    a = []
    b = []

    for text in texts:
        (b if random() > ratio else a).append(text)
    return a, b
