import math
import random
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
            #print "k value" +str(klist)
            binwidth=(xmax-xmin)/klist[j]
            for i in range(len(point_list)):
                for m in range(1,klist[j]+1):
                    if point_list[i][j] <= xmin+(m*binwidth):
                        point_list[i][j]=m
                        break

class Node:
    def __init__(self,majoritylabel):   
        self.left=None
        self.right=None
        self.value=None
        self.majoritylabel=majoritylabel
        self.left_value=None
        self.right_value=None

class Tree:
    def __init__(self):
        self.root=None
       
def calculate_impuritygain(trainsplit_list,attribute_pos):
    #print "trainsplitlist size"+str(len(zip(*trainsplit_list)))
    #print "attribute pos"+str(attribute_pos)
    attributeval_list=zip(*trainsplit_list)[attribute_pos]
    #print "attribute value list sum "+str(sum(attributeval_list))  #finds the sum of the columns but may cause error because sum cannot be performed for strings
    #print "attribute value list"+str(attributeval_list)
    label_list=zip(*trainsplit_list)[-1]
    print sum(label_list)
    #print "label list"+str(label_list)
    distinctattrval=sorted(set(attributeval_list))
    print "distinct attr val"+str(distinctattrval)
    root_impurity=calculate_impurity(label_list)
    #print "root impurity"+str(root_impurity)
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
        #print "tempsplit_impurity"+str(tempsplitval_impurity)
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
    #print "label dict"+str(countkeeper)
    for pair in countkeeper.items():
        sqsum+=(float(pair[1])/len(label_list))**2
    impurity=0.5*(1-sqsum)
    return impurity
 
def randomforest(temptrainlist,attribute_list,k):
    print "attribute list "+str(attribute_list)
    maxgain=0
    distinctattrval=[]
    pos=-1
    selattributelist=[]
    tempattribute_list=copy.deepcopy(attribute_list)
    for i in range(k):
        while sorted(set(tempattribute_list))[0]==0: 
            m=random.randint(0,len(attribute_list)-1)
            if (tempattribute_list[m]==0 and m not in selattributelist):
                selattributelist.append(m)
                tempattribute_list[m]=1
                break
    print "random select attribute "+str(selattributelist)
    for attrpos in selattributelist:
        tempdistinctattrval,tempgain=calculate_impuritygain(temptrainlist,attrpos)
        if tempgain>maxgain:
            maxgain=tempgain
            distinctattrval=tempdistinctattrval
            pos=attrpos
    print "maxgain "+str(maxgain) + " position "+str(pos)
    if maxgain!=0 and pos!=-1:
        attribute_list[pos]=1
        treenode=Node(getmajoritylabel(temptrainlist))
        treenode.value=pos
        #for j in range(len(disinctattrval)):    #use only if the code supports more than a single split and update the class structure instead of accepting left and right its prefered to accept an
        #dictionary where the keys are the values of the attributeval and value is the node reference to the code
        if len(distinctattrval)==1:
            treenode.left_value=distinctattrval[0]
        elif len(distinctattrval)==2:
            treenode.left_value=distinctattrval[0]
            treenode.right_value=distinctattrval[1]
        lefttrainlist=[]
        righttrainlist=[]
        for items in temptrainlist:
            #print "items "+str(items[pos])+" distinct attr val "+str(disinctattrval[0])            
            if len(distinctattrval)==1:
                if items[pos]==distinctattrval[0]:
                    lefttrainlist.append(items)
            elif len(distinctattrval)==2:
                if items[pos]==distinctattrval[0]:
                    lefttrainlist.append(items)
                elif items[pos]==distinctattrval[1]:
                    righttrainlist.append(items)
        #print "copy list size"+str(len(copy.deepcopy(attribute_list)))
        if len(lefttrainlist)!=0:
            treenode.left=randomforest(lefttrainlist,copy.deepcopy(attribute_list),k)
        if len(righttrainlist)!=0:
            treenode.right=randomforest(righttrainlist,copy.deepcopy(attribute_list),k)
        return treenode
#need to add the limiting condition to the recursion and either modify the class node structure or hardcode the values for just the binary values
    else:
        treenode=Node(getmajoritylabel(temptrainlist))
        return treenode

def getmajoritylabel(item_list):
    final_label_list=zip(*item_list)[-1]
    label_counter_dict={}
    for label in final_label_list:
        if label not in label_counter_dict:
            label_counter_dict[label]=1
        else:
            label_counter_dict[label]+=1
    majoritylabel_dict=sorted(label_counter_dict.items(),key=lambda x:x[1],reverse=True)
    print "majoritylabel_dict"+str(majoritylabel_dict)
    return majoritylabel_dict[0][0] 

def getclasslabel(treenode,item):
    if treenode.value!=None:
        pos=treenode.value
        if treenode.left_value==item[pos]:
            majoritylabel=getclasslabel(treenode.left,item)
            return majoritylabel
        if treenode.right_value==item[pos]:
            majoritylabel=getclasslabel(treenode.right,item)
            return majoritylabel
        else:
            return treenode.majoritylabel
    else:
        return treenode.majoritylabel

def getmajorityclasslabel(randomtreelist,item):
    classlabeldict={}
    for i in range(len(randomtreelist)):
        #print "random tree list nodes"+str(randomtreelist[i].root)
        label=getclasslabel(randomtreelist[i].root,item)
        if label not in classlabeldict:
            classlabeldict[label]=1
        else:
            classlabeldict[label]+=1
    majoritylabelset=classlabeldict.items()
    return majoritylabelset[0][0]

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

def average(inputlist):
    listsum=0
    count=0
    for i in range(len(inputlist)):
        if inputlist[i]!=None:
            listsum+=inputlist[i]
            count+=1
    return float(listsum)/count

if __name__=="__main__":
    global point_list,treegrowing_threshold
    point_list=[]
    loaddata('/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project3/project3_dataset1.txt')
    normalizedata() 
    discsplitvalue=2
    k=[discsplitvalue]*(len(point_list[0])-1)
    discretize(k)
    attribute_list=[0]*(len(point_list[0])-1)
    #f=open('output.txt','w')
    for value in point_list:
        #f.write(str(value)+"\n\n")
        print str(value)+"\n"
    #f.close
    nooftrees=3
    randomattrsel=3
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
        #print "length of the test set"+str(len(testpoint_list))
        randomtrees=[]
        for i in range(nooftrees):
            randomtrees.append(Tree())
            randomtrees[i].root=randomforest(trainpoint_list,copy.deepcopy(attribute_list),randomattrsel)
            print "random list root values "+str(randomtrees[i].root)
        predictedlabellist=[]
        for testitem in testpoint_list:
            predictedlabel=getmajorityclasslabel(randomtrees,testitem)
            #print str(predictedlabel)+"---"+str(testitem[-1])
            predictedlabellist.append(predictedlabel)
        confusionlist=calculate_confusionlist(list(zip(*testpoint_list)[-1]),predictedlabellist)
        accuracylist.append(calculateperformancemetric(confusionlist,"accuracy"))
        precisionlist.append(calculateperformancemetric(confusionlist,"precision"))
        recalllist.append(calculateperformancemetric(confusionlist,"recall"))
        fmeasurelist.append(calculateperformancemetric(confusionlist,"fmeasure"))
    print "\n\n"
    print "Discretisation value "+str(discsplitvalue)
    print "Random tree selection value "+str(nooftrees)
    print "Random attribute selectiuon value "+str(randomattrsel)
    print "\n\n-------------------------------preformance metric values----------------------------------\n\n"
    #print "Accuracy for each fold "+str(accuracylist)
    print "Average accuracy "+str(average(accuracylist))
    #print "Precision for each fold " + str(precisionlist)
    print "Average precion " +str(average(precisionlist)) 
    #print "Recall for each fold " + str(recalllist)
    print "Average Recall " +str(average(recalllist))
    #print "Fmeasure for each fold "+ str(fmeasurelist)
    print "Average fmeasure "+str(average(fmeasurelist))







