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
    def __init__(self,value):   
        self.left=None
        self.right=None
        self.value=value
        self.left_value=None
        self.right_value=None

class Tree:
    def __init__(self):
        self.root=None
        
def calculate_impuritygain(trainsplit_list,attribute_pos):
    print "trainsplitlist size"+str(len(zip(*trainsplit_list)))
    print "attribute pos"+str(attribute_pos)
    attributeval_list=zip(*trainsplit_list)[attribute_pos]
    #print "attribute value list sum "+str(sum(attributeval_list))  #finds the sum of the columns but may cause error because sum cannot be performed for strings
    print "attribute value list"+str(attributeval_list)
    label_list=zip(*trainsplit_list)[-1]
    #print sum(label_list)
    print "label list"+str(label_list)
    distinctattrval=sorted(set(attributeval_list))
    print "distinct attr val"+str(distinctattrval)
    root_impurity=calculate_impurity(label_list)
    print "root impurity"+str(root_impurity)
    attrsplitval_impurity_list=[]
    attrsplit_labellist=[]
    for val in distinctattrval:
        templabel_list=[]
        tempsplitval_impurity=0
        for items in trainsplit_list:
            if items[attribute_pos]==val:
                #print "inside condition"
                templabel_list.append(items[-1])
        attrsplit_labellist.append(templabel_list)
        #print "templabel_list"+str(sum(templabel_list))
        tempsplitval_impurity=calculate_impurity(templabel_list)
        print "tempsplit_impurity"+str(tempsplitval_impurity)
        attrsplitval_impurity_list.append(tempsplitval_impurity)
    totalsplit_impurity=0
    for i in range(len(attrsplitval_impurity_list)):
       totalsplit_impurity+=(float(len(attrsplit_labellist[i]))/len(trainsplit_list))*attrsplitval_impurity_list[i]
    print "total split impurity"+str(totalsplit_impurity)
    impurity_gain=root_impurity-totalsplit_impurity
    return (distinctattrval,impurity_gain)

def calculate_impurity(label_list):
    countkeeper={}
    for i in label_list:
        if i not in countkeeper:
            countkeeper[i]=1
        else:
            countkeeper[i]+=1
    sqsum=0
    print "label dict"+str(countkeeper)
    for pair in countkeeper.items():
        sqsum+=(float(pair[1])/len(label_list))**2
    impurity=0.5*(1-sqsum)
    return impurity
        
def CART(temptrain_list,attribute_list,treenode):
    print "hi"
    global treegrowing_threshold
    maxgain=0
    distinctattrval=[]
    pos=-1
    for i in range(len(attribute_list)):
        if attribute_list[i] != 0:
            tempdistinctattrval,tempgain=calculate_impuritygain(temptrain_list,i)
            print "tempgain"+str(tempgain)
            if tempgain>maxgain:
                maxgain=tempgain
                distinctattrval=tempdistinctattrval
                pos=i
    print "position max"+str(pos)
    if maxgain>=treegrowing_threshold and maxgain!=0 and pos!=-1:
        attribute_list[pos]=0
        treenode=Node(pos)
        #for j in range(len(disinctattrval)):    #use only if the code supports more than a single split and update the class structure instead of accepting left and right its prefered to accept an
        #dictionary where the keys are the values of the attributeval and value is the node reference to the code
        if len(distinctattrval)==1:
            treenode.left_value=distinctattrval[0]
        if len(distinctattrval)==2:
            treenode.right_value=distinctattrval[1]
        lefttrainlist=[]
        righttrainlist=[]
        for items in temptrain_list:
            #print "items "+str(items[pos])+" distinct attr val "+str(disinctattrval[0])            
            if len(distinctattrval)==1:
                if items[pos]==distinctattrval[0]:
                    lefttrainlist.append(items)
            if len(distinctattrval)==2:
                if items[pos]==distinctattrval[1]:
                    righttrainlist.append(items)
        #print "copy list size"+str(len(copy.deepcopy(attribute_list)))
        if len(lefttrainlist)!=0:
            CART(lefttrainlist,copy.deepcopy(attribute_list),treenode.left)
        if len(righttrainlist)!=0:
            CART(righttrainlist,copy.deepcopy(attribute_list),treenode.right)
#need to add the limiting condition to the recursion and either modify the class node structure or hardcode the values for just the binary values


if __name__=="__main__":
    global point_list,treegrowing_threshold
    point_list=[]
    loaddata('/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project3/project3_dataset2.txt')
    normalizedata()
    k=[2]*(len(point_list[0])-1)
    discretize(k)
    attribute_list=[1]*(len(point_list[0])-1)
    treegrowing_threshold=0.003
    f=open('output.txt','w')
    for value in point_list:
        f.write(str(value)+"\n\n")
        print str(value)+"\n"
    f.close
    maintree = Tree()
    CART(point_list,attribute_list,maintree.root)
    #print calculate_impuritygain(point_list,2)
