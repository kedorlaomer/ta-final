# encoding: utf-8

# use naïve bayes classifier for learning spam/ham

import os
from features import featuresForMail
from helpers import listdir_fullpath
from nltk.classify import NaiveBayesClassifier

def trainNaiveBayes(spamdir, hamdir):
    allFeatures = []
    classifications = []

    for f in listdir_fullpath(spamdir):
        allFeatures += [featuresForMail(f)]
        classifications += [True]

    for f in listdir_fullpath(hamdir):
        allFeatures += [featuresForMail(f)]
        classifications += [False]

    features = zip(allFeatures, classifications)
    classi = NaiveBayesClassifier.train(features)
    return classi
