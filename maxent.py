# encoding: utf-8

# use maximum entropy classifier for learning spam/ham

import os
from features import featuresForMail
from nltk.classify import MaxentClassifier

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def trainMaxEnt(spamdir, hamdir):
    allFeatures = []
    classifications = []

    for f in listdir_fullpath(spamdir):
        allFeatures += [featuresForMail(f)]
        classifications += [True]

    for f in listdir_fullpath(hamdir):
        allFeatures += [featuresForMail(f)]
        classifications += [False]

    features = zip(allFeatures, classifications)
    classi = MaxentClassifier.train(features)
    return classi
