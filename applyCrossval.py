# encoding=utf-8
 
from nbay import trainNaiveBayes
from helpers import listdir_fullpath
from features import featuresForMail
from sys import argv

# do cross validation on training/testing data

if __name__ == '__main__':
    if len(argv) == 3:
        hamdir = argv[1] + '/ham'
        spamdir = argv[2] + '/spam'
        classi = trainNaiveBayes(hamdir, spamdir)

        total = 0
        good = 0

        for f in listdir_fullpath(argv[1] + '/ham'):
            features = featuresForMail(f)
            total += 1
            if classi.classify(features) == False:
                good += 1

        for f in listdir_fullpath(argv[1] + '/spam'):
            features = featuresForMail(f)
            total += 1
            if classi.classify(features) == True:
                good += 1

        print "accuracy: " + str(float(int(float(good)/float(total)*10000))/100) + "%"

    else:
        print "usage: python applyCrossval.py <training directory> <testing directory>"
