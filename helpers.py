# encoding=utf-8

import os


def getDirContent(dirpath):

    content = []

    try:
        directoryListing = os.listdir(dirpath)
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
