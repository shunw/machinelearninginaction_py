# -*- coding: utf-8 -*-
import operator
from numpy import *
import re

def loadDataSet():
	postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'], 
					['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'], 
					['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
					['stop', 'posting', 'stupid', 'worthless', 'garbage'], 
					['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
					['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
	classVec = [0, 1, 0, 1, 0, 1]
	return postingList, classVec

def createVocabList(dataSet):
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
		# print vocabSet
	# print vocabSet
	return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print 'the word: %s is not in my Vocabulary!' % word
	return returnVec

def bagOfWords2VecMN(vocabList, inputSet):
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1
	return returnVec

def trainNB0(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])	#for the training matrix first row's word qty
	pAbusive = sum(trainCategory)/float(numTrainDocs)	#abusive number/ total line which is total document／所有的差评出现的频数
	p0Num = ones(numWords); p1Num = ones(numWords)	#make an array with the numwords qty len
	p0Denom = 2.0; p1Denom = 2.0
	# ?? 为何底数改变什么的不会影响最终结果？
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p1Vect = log(p1Num/p1Denom)	#在好的评价里，出现的相关单词的频数，计算为：相关单词的出现总次数／好的评价的所有的字数
	p0Vect = log(p0Num/p0Denom)	#同上
	return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
	# 参数依次为：已转为01array的文档[[...],[...], ...]; 差评词的概率array；好评词的概率array；差评的概率
	# ?? 为何p1和p0是酱紫计算？
	p1 = sum(vec2Classify*p1Vec)+log(pClass1)
	p0 = sum(vec2Classify*p0Vec)+log(1.0-pClass1)
	if p1 > p0:
		return 1
	else:
		return 0

def testingNB():
	listOPosts, listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
	p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses)) #得到条件概率，好的评价里，相关单词出现的频数；差评里，相关单词出现的频数；差评的频数
	testEntry = ['love', 'my', 'dalmation']	#进行测试
	thisDoc = array(setOfWords2Vec(myVocabList, testEntry)) #以training里出现的单词为基准进行测试，将testentry里的字以myvocablist为基准，转化成0/1 array
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)	
	testEntry = ['stupid', 'garbage']
	thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)

def textParse(bigString):
	import re
	listOfTokens = re.split(r'\W*', bigString)
	return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
	docList = []; classList = []; fullText = []
	for i in range(1, 26):
		wordList = textParse(open('email/spam/%d.txt' %i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(open('email/ham/%d.txt' %i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = createVocabList(docList)
	trainingSet = range(50); testSet = []
	for i in range(10):
		randIndex = int(random.uniform(0, len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat = []; trainClasses = []
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
	errorCount = 0
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList, docList[docIndex])
		if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
			errorCount += 1
	print 'the error rate is: ', float(errorCount)/len(testSet)


if __name__ == '__main__':
	# listOPosts, listClasses = loadDataSet()
	# myVocabList = createVocabList(listOPosts)
	# trainMat = []
	# for postinDoc in listOPosts:
	# 	trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
	# 	p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
	# p0V, p1V, pAb = trainNB0(trainMat, listClasses)
	# print p1V
	# testingNB()
	# print p0V, p1V, pAb
	
	# mySent = 'This book is the best book on Python or M.L. I have ever laid eyes upon. '
	# regEx = re.compile('\\W*')
	# listOfTokens = regEx.split(mySent)
	# print [tok.lower() for tok in listOfTokens if len(tok) > 0]
	
	# spamTest()
	import feedparser
	ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
	test = ny['entries']
	print len(test)