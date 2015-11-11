# -*- coding: utf-8 -*-
from numpy import *
import matplotlib.pyplot as plt

def loadDataSet():
	dataMat = []; labelMat = []
	fr = open('testSet.txt')
	for line in fr.readlines():
		lineArr = line.strip().split()
		dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
		labelMat.append(int(lineArr[2]))
	return dataMat, labelMat

def sigmoid(inX):
	return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, classLabels):
	dataMatrix = mat(dataMatIn)
	labelMat = mat(classLabels).transpose()
	m, n = shape(dataMatrix)
	alpha = .001
	maxCycles = 500
	weights = ones((n, 1))
	for k in range(maxCycles):
		h = sigmoid(dataMatrix*weights)
		error = (labelMat-h)
		weights = weights+alpha*dataMatrix.transpose()*error
	return weights

def stocGradAscent0(dataMatrix, classLabels):
	m, n = shape(dataMatrix)
	alpha = .01
	weights = ones(n)
	for i in range(m):
		h = sigmoid(sum(dataMatrix[i]*weights))
		error = classLabels[i]-h
		weights = weights+alpha*error*dataMatrix[i]
	return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
	m,n = shape(dataMatrix)
	weights = ones(n)
	for j in range(numIter):
		dataIndex = range(m)
		for i in range(m):
			alpha = 1/(1.0+j+i)+.01
			randIndex = int(random.uniform(0, len(dataIndex)))
			h = sigmoid(sum(dataMatrix[randIndex]*weights))
			error = classLabels[randIndex]-h
			weights = weights+alpha*error*dataMatrix[randIndex]
			del(dataIndex[randIndex])
	return weights



def plotBestFit(weights):
	# weights = wei.getA()	# return self as an [ndarray] obeject.
	dataMat, labelMat = loadDataSet()
	dataArr = array(dataMat)
	n = shape(dataArr)[0]	# get the row number
	xcord1 = []; ycord1 = []
	xcord2 = []; ycord2 = []
	for i in range(n):
		if int(labelMat[i]) == 1:	#过滤出label为1的信息
			xcord1.append(dataArr[i,1])	# x坐标为第一列
			ycord1.append(dataArr[i,2])	# y坐标为第二列
		else: 
			xcord2.append(dataArr[i, 1])
			ycord2.append(dataArr[i, 2])
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
	ax.scatter(xcord2, ycord2, s=30, c='green', marker='<')
	x = arange(-3.0, 3.0, 0.1)
	y = (-weights[0]-weights[1]*x)/weights[2]
	ax.plot(x, y)
	plt.xlabel('X1')
	plt.ylabel('X2')
	plt.show()



if __name__ == '__main__':
	# dataArr, labelMat = loadDataSet()
	
	# weights = gradAscent(dataArr, labelMat)
	# plotBestFit(weights.getA())

	# weights = stocGradAscent0(array(dataArr), labelMat)
	# plotBestFit(weights)

	# weights = stocGradAscent1(array(dataArr), labelMat)
	# plotBestFit(weights)
	train_fl = 'horseColicTraining.txt'
	test_fl = 'horseColicTest.txt'
	handler = open(train_fl)
	train_label = []; train_arr = []
	
	for lineArr in handler:
		lineArr = line.strip().split()
		dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
		labelMat.append(int(lineArr[2]))