import math

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

def discretize(klist):
	global point_list
	for j in range(len(point_list[0])-1):#-1 for excluding the last column for not considering the class label
		if type(zip(*point_list)[j][0]) is not str:#if its string doing nothing as they are already discritized
			xmin=min(zip(*point_list)[j])
			xmax=max(zip(*point_list)[j])
			binwidth=(xmax-xmin)/k[j]
			for i in range(len(point_list)):
				for m in range(1,k[j]+1):
					if point_list[i][j] <= xmin+(m*binwidth):
						point_list[i][j]=m
						break

class Node:
	def	__init__(self,value):	
		self.left=None
		self.right=None
		self.value=value
		self.left_value=None
		self.right_value=None

class Tree:
	def __init__(self,root):
		self.root=root

if __name__=="__main__":
	global point_list
	point_list=[]
	loaddata('/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project3/project3_dataset2.txt')
	normalizedata()
	k=[2]*(len(point_list))
	discretize(k)
	f=open('output.txt','w')
	for value in point_list:
		f.write(str(value)+"\n\n")
		print str(value)+"\n"
	f.close
	
