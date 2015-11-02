# <<<<<<< HEAD
from math import log
import operator

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): 
        	labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2) #log base 2
    return shannonEnt
    
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0])-1 #how many cols there, and minus the last col
	baseEntrop = calcShannonEnt(dataSet)
	bestInfoGain = 0.0; bestFeature = -1
	for i in range(numFeatures):
		feaList = [example[i] for example in dataSet]
		uniqueVals = set(feaList)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob*calcShannonEnt(subDataSet)
		infoGain = baseEntrop-newEntropy
		if (infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature

def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys(): classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]

def createTree(dataSet, labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0] #the last two if all others are same. 
	if len(dataSet[0]) == 1:
		return majorityCnt(classList) #the last two if sentence is just one element remaining. 
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
	return myTree

my_data, labels = createDataSet()
# print chooseBestFeatureToSplit(my_data)
# print my_data
# print my_data
from math import log
import operator
import treePlotter

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): 
        	labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2) #log base 2
    return shannonEnt
    
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0])-1 #how many cols there, and minus the last col
	baseEntrop = calcShannonEnt(dataSet)
	bestInfoGain = 0.0; bestFeature = -1
	for i in range(numFeatures):
		feaList = [example[i] for example in dataSet]
		uniqueVals = set(feaList)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob*calcShannonEnt(subDataSet)
		infoGain = baseEntrop-newEntropy
		if (infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature

def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys(): classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]

def createTree(dataSet, labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1:
		return majorityCnt(classList) #the last two if sentence is just one element remaining. 
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	### following is to build the tree with the best Label
	myTree = {bestFeatLabel:{}}	#this step is to create a empty for the decision tree with the best Label. 
	del(labels[bestFeat])	#this is to delete labels' (which is a list) bestFeat element. maybe because it is already in the myTree dict as the last sentence. 
	featValues = [example[bestFeat] for example in dataSet]	# to find all the value under the best label (the col)
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]	#this is to return all the left labels (because the best one is deleted.)
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
	return myTree

def classify(inputTree, featLabels, testVec):
	firstStr = inputTree.keys()[0]
	secondDict = inputTree[firstStr]
	featInex = featLabels.index(firstStr)
	for key in secondDict.keys():
		if testVec[featInex] == key:
			if type(secondDict[key]).__name__ == 'dict':
				classLabel = classify(secondDict[key], featLabels, testVec)
			else:
				classLabel = secondDict[key]
	return classLabel

def storeTree(inputTree, filename):
	import pickle
	fw = open(filename, 'w')
	pickle.dump(inputTree, fw)
	fw.close()

def grabTree(filename):
	import pickle
	fr = open(filename)
	return pickle.load(fr)

if __name__ == '__main__':
	# my_data, labels = createDataSet()
	# print chooseBestFeatureToSplit(my_data)
	# print my_data

	# myTree = createTree(my_data, labels)
	# print myTree

	# print labels
	# myTree = treePlotter.retrieveTree(0)
	# print myTree
	# print classify(myTree, labels, [1, 0])
	# print classify(myTree, labels, [1, 1])
# >>>>>>> 0d7feff1b991ccc67834634f0f3ca07b5b5e7479

	# storeTree(myTree, 'classifierStorage.txt')
	# print grabTree('classifierStorage.txt')

	### example: parse tab-delimited lines
	## this is to make the dataset
	file_name = 'lenses.txt'
	raw = open(file_name)
	lenses_data = []
	for line in raw:
		lenses_data.append(line.rstrip().split('\t'))
	lenses_label = ['age', 'prescript', 'astigmatic', 'tearRate']

	## this is to make the decision tree
	lenses_tree = createTree(lenses_data, lenses_label)

	storeTree(lenses_tree, 'lenses_tree.txt')
	grabTree('lenses_tree.txt')