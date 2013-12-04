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
			tempval.append(float(word))
		global trainpoint_list
		trainpoint_list.append(tempval)
			
def distance(x,y,dtype):
	if(dtype=='euclidean'):
		sumsq=0
		for i in range(len(x)-1):
			sumsq=sumsq+math.pow((x[i]-y[i]),2)
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
		sorted_majoritylist=sorted(majoritylist.items(),key=lambda x: x[1])
		print majoritylist
		return sorted_majoritylist[0][0]
	
if __name__ == '__main__':
	global trainpoint_list
	trainpoint_list=[]
	loaddata('/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project3/project3_dataset1.txt')
	templist=copy.deepcopy(trainpoint_list[3:20])
	emp=nearest_neighbour(templist,trainpoint_list[2],4)
	print emp
	clas=findclass(emp,trainpoint_list[2])
	print clas
