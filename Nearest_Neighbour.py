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
        for i in range(len(neighbourlist)):
            if majoritylist.has_key(neighbourlist[i][-1]):
                majoritylist[neighbourlist[i][-1]]=majoritylist[neighbourlist[i][-1]]+1
            else:
                majoritylist[neighbourlist[i][-1]]=1
        sorted_majoritylist=sorted(majoritylist.items(),key=lambda x: x[1],reverse=True)
        print sorted_majoritylist
        return sorted_majoritylist[0][0]
    
if __name__ == '__main__':
    global point_list
    point_list=[]
    loaddata('/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project3/project3_dataset2.txt')
    normalizedata()
    print max(max(point_list,key=lambda x:max(x)))
    trainpoint_list=copy.deepcopy(point_list[3:20])
    testpoint_list=copy.deepcopy(point_list[20:40])
    emp=nearest_neighbour(trainpoint_list,testpoint_list[2],4)
    print emp
    clas=findclass(emp,testpoint_list[2])
    print clas
