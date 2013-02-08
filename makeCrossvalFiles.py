# encoding: utf-8

from sys import argv
from glob import glob
from shutil import copy
from random import shuffle


#takes all the files in f and chunks them randomly in 10 different groups.
#for each of this chunks it makes a testing file and the rest is the training file
#it return an iterator of tuples of training files in a list and testing files in a list
def makeCrossValidationGroups(f):
    shuffle(f)
    n = min(10, len(f))
    # TODO: ask Alfonso
    m = 1 + len(f) / 10
    rl = []
    for i in range(n):
        if i == 0:
            test = f[i * m:(i + 1) * m]
            train = f[(i + 1) * m:len(f)]
        elif i == n - 1:
            test = f[i * m:len(f)]
            train = f[: i * m]
        else:
            test = f[i * m:(i + 1) * m]
            train = f[: i * m] + f[(i + 1) * m:len(f)]
        rl.append((train, test))
    return rl


def mergeLists(ham, spam, where):
    assert(len(ham) == len(spam))

    for i in range(len(ham)):
        trainingHam = ham[i][0]
        for x in trainingHam:
            copy(x, "%strain%s/ham/%s" % (where, i, x.split('/')[1]))
        testHam = ham[i][1]
        for x in testHam:
            copy(x, "%stest%s/ham/%s" % (where, i, x.split('/')[1]))
        trainingSpam = spam[i][0]
        for x in trainingSpam:
            copy(x, "%strain%s/spam/%s" % (where, i, x.split('/')[1]))
        testSpam = spam[i][1]
        for x in testSpam:
            # TODO: ask Alfonso
            copy(x, "%stest%s/spam/%s" % (where, i, x.split('/')[1]))


if __name__ == '__main__':
    if len(argv) > 2:
        ham = glob(argv[1] + '*')
        spam = glob(argv[2] + '*')
        print ham
        print spam
        mergeLists(
            makeCrossValidationGroups(ham),
            makeCrossValidationGroups(spam),
            argv[3],
        )
    else:
        print "path to the files is needed"
