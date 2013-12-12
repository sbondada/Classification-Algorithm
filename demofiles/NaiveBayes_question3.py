'''
@author: Navinderjeet Singh Mehrok
@author: Kaushal Bondada

For testing point 4
'''


from __future__ import division
#from cluster import KMeansClustering
import sys
import collections

features = []
classValueCounts = [0, 0]
metaData=[]
totalFeatures=0
avgPrecision=0.0
avgAccuracy= 0.0
avgRecall= 0.0
avgFMeasure=0.0
totPass=0
totFail=0

class feature:
    def __init__(self):
        self.min = 0
        self.max = 0
        self.values = []
        self.featureClass = []
        self.k = 2
        self.delta = 0.0
        self.newValueList = []
        self.newCountList = []  # have new discrete values as index eg 0,1 and have total counts for each of them
        self.featureCounts = collections.defaultdict(lambda: 1)
        self.strDict={}
        
    def addValues(self, value, assign,fType):
        if fType== "float":
            self.values.append(float(value))
        elif fType=="string":
            self.values.append(value)
        self.featureClass.append(int(assign))
        
        
    def shuffle(self):
        tempValues = list(self.values)
        tempValues.sort(key=float)
        self.max = tempValues[len(self.values) - 1]
        self.min = tempValues[0]
        self.delta = (self.max - self.min) / self.k
        
        center=int((len(self.values))/self.k)
        self.delta= tempValues[center]-self.min
        
        
    def assignFeature(self, value):
        val = float(value)
        #print self.min, self.max,self.delta,val
        if val <= self.min:
            return 0
        elif val >= self.max:
            return self.k - 1
        else:
                temp = self.min
                for i in range(self.k):
                    temp += (self.delta )
                    if val <= temp:
                        return i
        return (self.k-1)
    
    def updateDict(self):
        index=0
        for val in self.values:
            if val in self.strDict:
                index=self.strDict[val]
            else:
                index=len(self.strDict)
                self.strDict[val]=index
            
            if len(self.newCountList) <= index:
                self.newCountList.append(1)
                self.newValueList.append(index)
            else:
                self.newCountList[index]+=1
                self.newValueList.append(index)
                    
            
                
    def converter(self):
        for i in range(self.k):
            self.newCountList.append(0)
            self.featureCounts[i, 0] = 0
            self.featureCounts[i, 1] = 0  # initialize the feature and corresponding class count
        
        for counter in range(len(self.values)):
            self.newValueList.append(self.assignFeature(self.values[counter]))
            #print self.assignFeature(self.values[counter])
            self.newCountList[self.assignFeature(self.values[counter])] += 1
            self.featureCounts[self.assignFeature(self.values[counter]), self.featureClass[counter]] += 1
        


def getType(key):
    try:
        float(key)
        return "float"
    except:
        return "string"
    
def setMetaData(line):
    global totalFeatures, metaData
    line.rstrip('\n')
    attributes = line.split("\t")
    totalFeatures = len(attributes)-1
    for attr in attributes:
        try:
            float(attr)
            metaData.append("float")
        except:
            metaData.append("string")
    
def driver(trainData):
    global totalFeatures,metaData,classValueCounts,features
    setMetaData(trainData[0])

    features=[feature() for count in xrange(totalFeatures)]
    # now read the train file and update the values
    counter = 0
    for line in trainData:
        line.rstrip('\n')
        if line == "":
            continue
        readValues = line.split("\t")
        if float(readValues[len(readValues) - 1]) == 1:
            classValueCounts[1] += 1
        elif float(readValues[len(readValues) - 1]) == 0:
            classValueCounts[0] += 1
            
        for count in range(len(readValues) - 1):
            features[count].addValues(readValues[count], readValues[len(readValues) - 1],metaData[count])
        
    for count in range(totalFeatures):
        if metaData[count] == "float":
            features[count].shuffle()
            features[count].converter()
        elif metaData[count] == "string":
            features[count].updateDict()
    
    
    
def getClass(featureList):
    global classValueCounts
    totalTrainClasses = classValueCounts[0] + classValueCounts[1]
    prob = []
    for i in range(len(classValueCounts)):
        probH = 1.0
        probH = classValueCounts[i] / totalTrainClasses
        probX = 1.0
        probXgivenH = 1.0
        for j in range(len(featureList)):
            temp = 0
            if getType(featureList[j])== "float": 
                ftvalue = features[j].assignFeature(featureList[j])
            elif getType(featureList[j])== "string":
                if featureList[j] in features[j].strDict:
                    ftvalue= features[j].strDict[featureList[j]]
                else:
                    ftvalue=-1
            for count in features[j].newCountList:
                temp += count
            if ftvalue==-1:
                probX = float(probX * (1 / temp))
                probXgivenH = probXgivenH * (1 / classValueCounts[i])
            else:
                if features[j].newCountList[ftvalue]==0:
                    features[j].newCountList[ftvalue]=1
                probX = float(probX * (float((features[j].newCountList[ftvalue]) / temp)))
                probXgivenH = probXgivenH * (features[i].featureCounts[ftvalue, i] / classValueCounts[i])
        temp = (probXgivenH * probH) / probX
        prob.append(temp)
    print "probability for class 0:",prob[0]
    print "probability for class 1:",prob[1]
    if prob[0]>=prob[1]:
        return 0
    else:
        return 1    

def testMethod(testFile):
    
    global avgPrecision,avgAccuracy,avgRecall,avgFMeasure
    global totPass, totFail
    counter = 0
    passed=0
    failed=0
    matrixA=1
    matrixB=1
    matrixC=1
    matrixD=1
    for line in testFile:
        if line == "":
            continue
        featureList = []
        line.rstrip('\n')
        temp = line.split("\t")
        #print temp
        #actual=int(temp[len(temp)-1])
        actual=0
        for i in range(len(temp) - 1):
            featureList.append(temp[i])
        expected=getClass(featureList)
        if expected== 1:
            if actual== expected:
                matrixA+=1
                passed+=1
            elif actual ==0 and expected ==1:
                matrixC+=1
                failed+=1
        elif expected==0:
            if actual== 0:
                passed+=1
                matrixD+=1
            else:
                failed+=1
                matrixB+=1
        
    totPass=totPass+ passed
    totFail= totFail+ failed
    accuracy= (matrixA + matrixD)/(matrixA+matrixB+matrixC+matrixD)
    precision= matrixA/(matrixA+matrixC)
    recall= matrixA/(matrixA+matrixB)
    FMeasure= (2*matrixA)/(2*matrixA+matrixB+matrixC)
    avgPrecision= avgPrecision+ precision
    avgAccuracy= avgAccuracy+ accuracy
    avgRecall= avgRecall+ recall
    avgFMeasure=avgFMeasure+ FMeasure
    #print "Pass:",passed,"\nFail:",failed


if __name__ == '__main__':
    #global classValueCounts, metaData
    #filename= "dataset.txt"
    '''
    filename= sys.argv[1]
    lines = open(filename).read().splitlines()
    BinSize=int((len(lines)/10))
    for i in range(10):
        classValueCounts=[0,0]
        metaData=[]
        
        j=i+1
        testData=[]
        trainData=[]
        print "*********Iter:",j," *********"
        for line in range(len(lines)):
            if lines[line] == "":
                continue
            if line < (j*BinSize) and line >=(i*BinSize) :
                testData.append(lines[line])
            elif j==10 and line >=(i*BinSize):
                testData.append(lines[line])
            else:
                trainData.append(lines[line])
        print "Train data size", len(trainData)
        print "Test data size", len(testData)
        driver(trainData)
        testMethod(testData)
        #testLines = open(testFilename).read().splitlines()
    '''
    trainFilename= sys.argv[1]
    trainLines = open(trainFilename).read().splitlines()
    
    driver(trainLines)
    
    testFilename= sys.argv[2]
    
    testLines= ["sunny\tcool\thigh\tstrong\t0"]
    
    testMethod(testLines)
    '''
    print "\n"
    print "Pass Percentage:", round(totPass/(totPass+totFail)*100)
    print "Precision:\t",avgPrecision
    print "Accuracy:\t",avgAccuracy
    print "Recall:\t\t",avgRecall
    print "F measure:\t",avgFMeasure
    print "Total Pass:\t", totPass,"\nTotal Fail:\t", totFail
    '''
    
