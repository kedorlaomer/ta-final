# encoding=utf-8

from os import listdir
import os
from random import random


def getDirContent(dirpath):

    content = []

    try:
        directoryListing = listdir(dirpath)
        for filepath in directoryListing:
            with open("%s/%s" % (dirpath, filepath), 'r') as f:
                content.append(f.read())
    except Exception as ex:
        print 'Error occured while reading directory:', ex

    return content


def getHamContent():
    return getDirContent('trainingham')


def getSpamContent():
    return getDirContent('trainingspam')

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def splitByRatio(texts, ratio):

    a = []
    b = []

    for text in texts:
        (b if random() > ratio else a).append(text)
    return a, b
