'''
Created on Nov 25, 2013

@author: kaushal
'''
import math
import copy

def loaddata(filename):
    tempval=[]
    inpfile=open(filename,'r')
    for line in inpfile:
        tempval=[]
        sp=line.split("\t")
        for word in sp:
            try:
                tempval.append(float(word))
            except ValueError:
                tempval.append(word)
        global point_list
        point_list.append(tempval)


def normalizedata():
    global point_list
    for j in range(len(point_list[0])-1):#-1 for not considering the last column for the calculations   
        for i in range(len(point_list)):
            if type(point_list[i][j]) is not str:
                point_list[i][j]=(point_list[i][j]-min(zip(*point_list)[j]))/(max(zip(*point_list)[j])-min(zip(*point_list)[j])) #normalizing the data in the range of (0,1)

def distance(x,y,dtype):
    if(dtype=='euclidean'):
        sumsq=0
        for i in range(len(x)-1):
            if type(x[i]) is not str:
                sumsq+=math.pow((x[i]-y[i]),2)
            else:
                if x[i]==y[i]:
                    sumsq+=1
                else:
                    sumsq+=0
            dist=math.sqrt(sumsq)
    return dist  

def nearest_neighbour(temptrainpoint_list,testpoint,k):
    nearestneighbor_list=[]
    for i in range(k):
        mindist=float('inf')
        minpos=-1
        for trainpointindex in range(len(temptrainpoint_list)):
            result=distance(testpoint,temptrainpoint_list[trainpointindex],'euclidean')
            if mindist>result:      
                mindist=result
                minpos=trainpointindex
        if minpos!=-1:
            nearestneighbor_list.append(temptrainpoint_list[minpos])
            temptrainpoint_list.pop(minpos)
    return nearestneighbor_list

def findclass(neighbourlist,testpoint):
        majoritylist=dict()
        print "neighboring list "+str(len(neighbourlist))
        for i in range(len(neighbourlist)):
            if majoritylist.has_key(neighbourlist[i][-1]):
                majoritylist[neighbourlist[i][-1]]=majoritylist[neighbourlist[i][-1]]+1
            else:
                majoritylist[neighbourlist[i][-1]]=1
        sorted_majoritylist=sorted(majoritylist.items(),key=lambda x: x[1],reverse=True)
        print "majority list "+str(sorted_majoritylist)
        return sorted_majoritylist[0][0]
    
def calculate_confusionlist(actual_labellist,predicted_labellist):
    TP , FN , FP , TN = 0 , 0 , 0 , 0
    for inc in range(len(predicted_labellist)):
        if actual_labellist[inc]==1.0:
            if predicted_labellist[inc]==1.0:
               TP+=1
            elif predicted_labellist[inc]==0.0:
                FN+=1
        elif actual_labellist[inc]==0.0:
            if predicted_labellist[inc]==1.0:
                FP+=1
            if predicted_labellist[inc]==0.0:
                TN+=1
    return list((TP,FN,FP,TN)) 

def calculateperformancemetric(confusion_list,metric):
    a,b,c,d=(confusion_list)
    if metric=="accuracy":
        accuracy=float(a+d)/(a+b+c+d)
        return accuracy
    if metric=="precision":
        try:
            precision=float(a)/(a+c)
        except:
            precision=None
        return precision
    if metric=="recall":
        try:
            recall=float(a)/(a+b)
        except:
            recall=None
        return recall
    if metric=="fmeasure":
        try:
            p=float(a)/(a+c)
            r=float(a)/(a+b)
            fmeasure=float(2*r*p)/(r+p)
        except:
            fmeasure=None
        return fmeasure

if __name__ == '__main__':
    global point_list
    point_list=[]
    loaddata('/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project3/project3_dataset1.txt')
    normalizedata()
    #print max(max(point_list,key=lambda x:max(x)))
    looplist=range(0,len(point_list),len(point_list)/10)
    looplist.pop(-1)
    looplist.append(len(point_list))
    accuracylist=[]
    precisionlist=[]
    recalllist=[]
    fmeasurelist=[]
    for inc in range(len(looplist)-1):
        trainpoint_list_first=point_list[:looplist[inc]]
        testpoint_list=point_list[looplist[inc]:looplist[inc+1]]
        trainpoint_list_second=point_list[looplist[inc+1]:]
        trainpoint_list=trainpoint_list_first+trainpoint_list_second
        predictedlabellist=[]
        for testitem in testpoint_list:
            nnlist=nearest_neighbour(copy.deepcopy(trainpoint_list),testitem,5)
            predictedlabel=findclass(nnlist,testpoint_list[2])
            predictedlabellist.append(predictedlabel)
        confusionlist=calculate_confusionlist(list(zip(*testpoint_list)[-1]),predictedlabellist)
        accuracylist.append(calculateperformancemetric(confusionlist,"accuracy"))
        precisionlist.append(calculateperformancemetric(confusionlist,"precision"))
        recalllist.append(calculateperformancemetric(confusionlist,"recall"))
        fmeasurelist.append(calculateperformancemetric(confusionlist,"fmeasure"))
    print "accuracy for each fold "+str(accuracylist)
    print "average accuracy"+str(float(sum(accuracylist))/len(accuracylist))
    print "precision for each fold " + str(precisionlist)
    print "recall for each fold " + str(recalllist)
    print "fmeasure for each fold "+ str(fmeasurelist)
