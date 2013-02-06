# encoding: utf-8

from sys import argv
from glob import glob
from random import shuffle
from shutil import copy

#takes all the files in f and chunks them randomly in 10 different groups.
#for each of this chunks it makes a testing file and the rest is the training file
#it return an iterator of tuples of training files in a list and testing files in a list
def makeCrossValidationGroups(f):
    shuffle(f)
    n = 10 if len(f)>=10 else len(f)
    m = max(len(f)/10,1)
    rl = []
    for i in range(n):
        if i == 0:
        	test = f[i*m:(i+1)*m]
        	train = f[(i+1)*m:len(f)]
        elif i==n-1:
            test = f[i*m:len(f)]
            train = f[0 : i*m]
        else : 
            test = f[i*m:(i+1)*m]
            train = f[0 : i*m] + f[(i+1)*m:len(f)] 
        rl.append((train,test))
    return rl

def mergeLists(ham,spam,where):
	if len(ham) == len(spam):
		for i in range(len(ham)):
			trainingHam = ham[i][0]			
			for x in trainingHam:
				copy(x,where+'train'+str(i)+'/ham/'+x.split('/')[1])
			testHam = ham[i][1]
			for x in testHam:
				copy(x,where+'test'+str(i)+'/ham/'+x.split('/')[1])
			trainingSpam = spam[i][0]
			for x in trainingSpam:
				copy(x,where+'train'+str(i)+'/spam/'+x.split('/')[1])			
			testSpam = spam[i][1]
			for x in testSpam:
				copy(x,where+'test'+str(i)+'/ham/'+x.split('/')[1])
	else:
		assert(False)


if __name__ == '__main__':
	if len(argv)>2:
		ham = glob(argv[1]+'*')
		spam = glob(argv[2]+'*')
		mergeLists(makeCrossValidationGroups(ham),makeCrossValidationGroups(spam),argv[3])
	else:

		print "path to the files is needed"
