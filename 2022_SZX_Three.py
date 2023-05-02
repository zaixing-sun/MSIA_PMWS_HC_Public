
'''
MSIA & HSA9Fs
'''


from cmath import inf
import os
from sys import get_asyncgen_hooks
from matplotlib import markers 
from numpy.lib.function_base import append, copy
from Class.VMScheduling import VMScheduling
from Class.SyntheticGenerator import SyntheticGenerator
from Class.VMType import VMType,PrivateCloudVMType
# from Class.PrivateCloudVMType import PrivateCloudVMType
from Class.Task import Task
from Class.File import File
import string
import math
import numpy as np
import re
import copy
import random
import matplotlib.pyplot as plt
import GlobalResource
# import GlobalWorkflow
import xlwings as xw
import time
import RandomlyGeneratedDAG_2002
from RandomlyGeneratedDAG_2002 import RandomlyGeneratedApplicationGraphs
import operator
# import setGlobalVar


def case1(self):
    '''
    Simplified DAG
    '''
    listNode = []
    setNode = set()
    for name,task in self.items():        
        tempName = name
        tempTask = task      
        tempList = set()  
        if not(tempName in setNode):            
            tempList = [tempName]
            while True:
                setNode.add(tempName)
                if (len(tempTask.outputs)==1):
                    if (len(self[tempTask.outputs[0].id].inputs)==1):
                        tempList.append(tempTask.outputs[0].id)
                        tempName = tempTask.outputs[0].id
                        tempTask = self[tempTask.outputs[0].id] 
                    else:
                        break 
                else:
                    break 
        if len(tempList)>1: 
            listNode.insert(len(listNode),tempList) 
    for i in range(len(listNode)):
        self[listNode[i][0]].addjobsetname(str(listNode[i][0]))
        self[listNode[i][0]].outputs.pop()
        self[listNode[i][0]].outputs = self[listNode[i][len(listNode[i])-1]].outputs         
        for j in range(1,len(listNode[i])):
            self[listNode[i][0]].MI +=self[listNode[i][j]].MI
            self[listNode[i][0]].runtime +=self[listNode[i][j]].runtime 
            # self[listNode[i][0]].storage +=self[listNode[i][j]].storage
            if j == len(listNode[i])-1:
                for k in range(len(self[listNode[i][j]].outputs)):
                    for h in range(len(self[self[listNode[i][j]].outputs[k].id].inputs)):
                        if self[self[listNode[i][j]].outputs[k].id].inputs[h].id==listNode[i][j]:
                           self[self[listNode[i][j]].outputs[k].id].inputs[h].changeID(listNode[i][0]) 
            self[listNode[i][0]].addjobsetname(self[listNode[i][0]].jobsetname+'_'+str(listNode[i][j]))
            self.pop(listNode[i][j])    


    list1 = [i for i in range(len(self))]
    listkey = list(self.keys())
    for i in list1:
        if self[listkey[i]].jobsetname == None:
            self[listkey[i]].jobsetname = str(listkey[i])
        if i != listkey[i]:
            for parent in self[listkey[i]].inputs:
                for p_child in self[parent.id].outputs:
                    if p_child.id == listkey[i]:
                        p_child.id = i
            if self[listkey[i]].outputs != []:
                for child in self[listkey[i]].outputs:
                    for c_parent in self[child.id].inputs:
                        if c_parent.id == listkey[i]:
                            c_parent.id = i               
            self[listkey[i]].id = i 
            self[i] = self.pop(listkey[i])


    # k = 0

def sortCaseNode(self,listNode):
    '''
    按照运行时间的降序排列
    '''
    for i in range(len(listNode)-1):
        for j in range(i+1,len(listNode)):
            if self[listNode[i]].runtime<self[listNode[j]].runtime:
                listNode[i],listNode[j] = listNode[j], listNode[i]

def case2(self):
    listNode = []
    for name,task in self.items():  
        if (len(task.outputs)>1):
            booleanFlag = True
            for each in range(len(task.outputs)):
                if (len(self[task.outputs[each].id].inputs)!=1):
                   booleanFlag = False
                   break
            if booleanFlag:  
                listNode.append(name)
    # sortCaseNode(self,listNode)

    listSucNode = []
    for i in range(len(listNode)):
        if set(self[listNode[i]].outputs):
            # listSucNode.insert(len(listSucNode), [])
            for j in range(len(self[listNode[i]].outputs)):
                listSucNode.append(self[listNode[i]].outputs[j].id)
            # sortCaseNode(self,listSucNode[i])   [len(listSucNode)-1]

    # listSucNode = []
    # for i in range(len(listNode)):
    #     if set(self[listNode[i]].outputs):
    #         listSucNode.insert(len(listSucNode), [])
    #         for j in range(len(self[listNode[i]].outputs)):
    #             listSucNode[len(listSucNode)-1].append(self[listNode[i]].outputs[j].id)
    #         # sortCaseNode(self,listSucNode[i])
    return  listNode, listSucNode         

def case3(self):
    listNode = []
    for name,task in self.items():  
        if (len(task.inputs)>1):
            booleanFlag = True
            for each in range(len(task.inputs)):
                if (len(self[task.inputs[each].id].outputs)!=1):
                   booleanFlag = False
                   break
            if booleanFlag:  
                listNode.append(name)
    # sortCaseNode(self,listNode)

    listPreNode = []
    for i in range(len(listNode)):
        if set(self[listNode[i]].inputs):
            # listPreNode.insert(len(listPreNode), [])
            for j in range(len(self[listNode[i]].inputs)):
                listPreNode.append(self[listNode[i]].inputs[j].id)
            # sortCaseNode(self,listPreNode[i])           [len(listPreNode)-1]

    # listPreNode = []
    # for i in range(len(listNode)):
    #     if set(self[listNode[i]].inputs):
    #         listPreNode.insert(len(listPreNode), [])
    #         for j in range(len(self[listNode[i]].inputs)):
    #             listPreNode[len(listPreNode)-1].append(self[listNode[i]].inputs[j].id)
    #         # sortCaseNode(self,listPreNode[i])
    return  listNode, listPreNode

def case4(self):
    '''
    Simplified DAG
    '''
    listNode = []
    setNode = set()
    for name,task in self.items():        
        tempName = name
        tempTask = task      
        tempList = set()  
        if not(tempName in setNode):            
            tempList = [tempName]
            while True:
                setNode.add(tempName)
                if (len(tempTask.outputs)==1):
                    if (len(self[tempTask.outputs[0].id].inputs)==1):
                        tempList.append(tempTask.outputs[0].id)
                        tempName = tempTask.outputs[0].id
                        tempTask = self[tempTask.outputs[0].id] 
                    else:
                        break 
                else:
                    break 
        if len(tempList)>1: 
            listNode.insert(len(listNode),tempList) 
    for i in range(len(listNode)):
        self[listNode[i][0]].addjobsetname(str(listNode[i][0]))
        self[listNode[i][0]].outputs.pop()
        self[listNode[i][0]].outputs = self[listNode[i][len(listNode[i])-1]].outputs         
        for j in range(1,len(listNode[i])):
            self[listNode[i][0]].MI +=self[listNode[i][j]].MI
            self[listNode[i][0]].runtime +=self[listNode[i][j]].runtime 
            if j == len(listNode[i])-1:
                for k in range(len(self[listNode[i][j]].outputs)):
                    for h in range(len(self[self[listNode[i][j]].outputs[k].id].inputs)):
                        if self[self[listNode[i][j]].outputs[k].id].inputs[h].id==listNode[i][j]:
                           self[self[listNode[i][j]].outputs[k].id].inputs[h].changeID(listNode[i][0]) 
            self[listNode[i][0]].addjobsetname(self[listNode[i][0]].jobsetname+'_'+str(listNode[i][j]))
            self.pop(listNode[i][j])        
    # k = 0


def taskTopologicalLevel(self):  
    setLevelNode = set() 
    dictNodeLevel = {}
    intflag = 0
    while True:
        for name,task in self.items():  
            if (not(name in setLevelNode)):
                if (len(task.inputs)==0):         
                    setLevelNode.add(name)
                    dictNodeLevel[name] = 0
                    intflag += 1     
                elif  (len(task.outputs)==0):   
                    setLevelNode.add(name)
                    dictNodeLevel[name] = -1
                    intflag += 1 
                else:
                    preNodedict = {}
                    for each in range(len(task.inputs)):
                        if task.inputs[each].id in setLevelNode:
                            preNodedict[task.inputs[each].id] = dictNodeLevel[task.inputs[each].id]
                        else:
                            break
                    if len(preNodedict)==len(task.inputs):
                        dictNodeLevel[name] = max(list(preNodedict.values()))+1
                        setLevelNode.add(name)
                        intflag += 1
        if intflag == len(self):
            break
    ## 以下是从源节点起分层
    DAGLevel = [[] for i in range(max(dictNodeLevel.values())+2)]  
    for key1,value1 in dictNodeLevel.items():
        if value1 == -1:
            DAGLevel[max(dictNodeLevel.values())+1].append(key1)
            self[key1].Level = max(dictNodeLevel.values())+1
        else:    
            DAGLevel[value1].append(key1)
            self[key1].Level = value1

    # '''以下是从根节点起分层 目前的7种工作流结构，
    #     只有适用于SIPHT工作流，其他工作流不受影响，
    #     故当SIPHT工作流效果不好时可以使用 '''
    # setLevelNode = set() 
    # dictNodeLevel = {}
    # intflag = 0
    # while True:
    #     for name,task in self.items():  
    #         if (not(name in setLevelNode)):
    #             if (len(task.outputs)==0):         
    #                 setLevelNode.add(name)
    #                 dictNodeLevel[name] = len(DAGLevel)-1
    #                 intflag += 1     
    #             elif  (len(task.inputs)==0):   
    #                 setLevelNode.add(name)
    #                 dictNodeLevel[name] = 0
    #                 intflag += 1 
    #             else:
    #                 sucNodedict = {}
    #                 for each in range(len(task.outputs)):
    #                     if task.outputs[each].id in setLevelNode:
    #                         sucNodedict[task.outputs[each].id] = dictNodeLevel[task.outputs[each].id]
    #                     else:
    #                         break
    #                 if len(sucNodedict)==len(task.outputs):
    #                     dictNodeLevel[name] = min(list(sucNodedict.values()))-1
    #                     setLevelNode.add(name)
    #                     intflag += 1
    #     if intflag == len(self):
    #         break
    # DAGLevel_RootNode = [[] for i in range(len(DAGLevel))]
    # for key1,value1 in dictNodeLevel.items():
    #     DAGLevel_RootNode[value1].append(key1)

    ## 按执行时间降序排列
    for k in range(len(DAGLevel)):
        for i in range(len(DAGLevel[k])-1):
            for j in range(i+1,len(DAGLevel[k])):
                if self[DAGLevel[k][i]].runtime<self[DAGLevel[k][j]].runtime:
                    DAGLevel[k][i],DAGLevel[k][j] = DAGLevel[k][j], DAGLevel[k][i]
    return DAGLevel

def LongestExecuteTime(self):
    """
    Rule3: longest execute time
    """
    for i in range(len(self)-1):
        for j in range(i+1,len(self)): 
            if SimplifiedWorkflow[self[i]].runtime<SimplifiedWorkflow[self[j]].runtime:
                self[i],self[j] = self[j],self[i]

def ShortestExecuteTime(self):
    """
    Rule4: shortest execute time
    """
    for i in range(len(self)-1):
        for j in range(i+1,len(self)): 
            if SimplifiedWorkflow[self[i]].runtime>SimplifiedWorkflow[self[j]].runtime:
                self[i],self[j] = self[j],self[i]

def getEST(self):
    NumPre = len(self.inputs)  #父节点的个数
    NumSuc = len(self.outputs) #子节点的个数  
    vmn = None                 #将要选择的VM
    taskcore = None            #将要选择的VM的核      
    EST = 0                 #最早开始时间
    listInputs = self.inputs
    # if NumPre>0:
    '''
    包含父节点的task，先计算最早可开始时间（所有父节点最晚的完工时间、相应的父节点）和对应的VM、父节点所在VM的完工时间
    最早可开始时间（Earliest Start Time, EST）      EST_VM(当跨VM时需要传输时间)
    父节点所在VM的完工时间

    在计算当前节点的开始时间时，要加上父节点的传输时间
    '''    
    VMNums = len(VMS)               
    listESTVM = []
    for j in range(VMNums):                     #listESTVM[j][k] 第j台VM的第k个核上的EST,最后在此列表中取最小的VM、核
        listESTVM.append([])
        for k in range(VMS[j].NumCores):
            listESTVM[j].append(VMS[j].CompleteTime[k])

    listEST = [[] for j in range(2)]            #0 = id (task)   1 = Finishtime     
    for j in range(NumPre):
        listEST[0].append(listInputs[j].id)
        listEST[1].append(SimplifiedWorkflow[listInputs[j].id].FinishTime)

        for j1 in range(VMNums):
            DataTransferRate = None
            if j1 == SimplifiedWorkflow[listEST[0][j]].VMnum:
                DataTransferRate = 0
            # elif   j1 < SimplifiedWorkflow[listEST[0][j]].VMnum:   ###     20210923更改
            elif   VMS[j1].id <= VMS[SimplifiedWorkflow[listEST[0][j]].VMnum].id:
                DataTransferRate = VMT.B[VMS[j1].id]
            else:
                DataTransferRate = VMT.B[VMS[ SimplifiedWorkflow[listEST[0][j]].VMnum].id]
            
            DataTransferTime = 0 if DataTransferRate == 0 else (listInputs[j].size/DataTransferRate * DTT)  #将传输时间放大DTT倍 
            
            startTimePreDTT = listEST[1][j]+DataTransferTime
            for k in range(VMS[j1].NumCores):
                listESTVM[j1][k] = max(listESTVM[j1][k],startTimePreDTT) #,VMS[j1].CompleteTime[k]

    if EachLevelVM != []:  ##  此处修改了下面一段的写法
        listX = [ min(listESTVM[j]) for j in EachLevelVM]
        # EST = min(listX)

        listX0 = [ round(min(listESTVM[j]),3) for j in EachLevelVM]
        EST0 = min(listX0)

        if listX0.count(EST0)>1:
            Difference = []
            for i in range(len(EachLevelVM)):
                if listX0[i]==EST0:
                    Difference.append([EachLevelVM[i],listX0[i]-min(VMS[EachLevelVM[i]].CompleteTime)])
                    #[[EachLevelVM[i],listX[i]-min(VMS[EachLevelVM[i]].CompleteTime)] for i in range(len(EachLevelVM))  ]
            Dif = sorted(Difference, key=lambda Difference: Difference[1])
            vmn = Dif[0][0] #listX.index(min(listX)) 
             
            for i1 in range(1,len(Dif)):
                if (Dif[i1][1] == Dif[0][1]) and (VMS[vmn].id<VMS[Dif[i1][0]].id):# 3):# and(vmn<Dif[0][0]+3): #GlobalResource.SuitVM):#
                    vmn = Dif[i1][0]
                    break
        else :
            vmn = EachLevelVM[listX.index(min(listX))]

        # vmn = EachLevelVM[listX.index(EST)]#[vmn]
        EST = min(listESTVM[vmn])
        if (EST+self.runtime/VMT.ProcessingCapacity[VMS[vmn].id]<=LevelMaxFinishTtime):
            taskcore = listESTVM[vmn].index(EST)
            return vmn,taskcore,EST

    if taskcore == None:
        listX = [ min(listESTVM[j]) for j in ListLevelVM]
        # EST = min(listX)

        listX0 = [ round(min(listESTVM[j]),3) for j in ListLevelVM]
        EST0 = min(listX0)

        if listX0.count(EST0)>1:
            Difference = []
            for i in range(len(ListLevelVM)):
                if listX0[i]==EST0:
                    Difference.append([ListLevelVM[i],listX0[i]-min(VMS[ListLevelVM[i]].CompleteTime)])
                    #[[ListLevelVM[i],listX[i]-min(VMS[ListLevelVM[i]].CompleteTime)] for i in range(len(ListLevelVM))  ]
            Dif = sorted(Difference, key=lambda Difference: Difference[1])
            vmn = Dif[0][0] #listX.index(min(listX))   
            for i1 in range(1,len(Dif)):
                if (Dif[i1][1] == Dif[0][1]) and (VMS[vmn].id<VMS[Dif[i1][0]].id):# 3):# and(vmn<Dif[0][0]+3): # GlobalResource.SuitVM):#
                    vmn = Dif[i1][0]
                    break
        else :
            vmn = ListLevelVM[listX.index(min(listX))]

        # vmn = ListLevelVM[listX.index(EST)]#[vmn]
        EST = min(listESTVM[vmn])
        if (EST+self.runtime/VMT.ProcessingCapacity[VMS[vmn].id]<=LevelMaxFinishTtime):
            taskcore = listESTVM[vmn].index(EST)
            return vmn,taskcore,EST

    if taskcore == None:
        listX = [ min(listESTVM[j]) for j in range(VMNums)] 
        # EST = min(listX) 

        listX0 = [ round(min(listESTVM[j]),3) for j in range(VMNums)]
        EST0 = min(listX0)

        if listX0.count(EST0)>1:
            Difference = []
            for i in range(VMNums):
                if listX0[i]==EST0:
                    Difference.append([i,listX0[i]-min(VMS[i].CompleteTime)]) #[[i,listX[i]-min(VMS[i].CompleteTime)] for i in range(VMNums)  ]
            Dif = sorted(Difference, key=lambda Difference: Difference[1])
            vmn = Dif[0][0] #listX.index(min(listX))
            for i1 in range(1,len(Dif)):
                if (Dif[i1][1] == Dif[0][1]) and (VMS[vmn].id<VMS[Dif[i1][0]].id):# 3):#  and(vmn<Dif[0][0]+3): # GlobalResource.SuitVM):#
                    vmn = Dif[i1][0]
                    break
        else :
            vmn = listX.index(min(listX))  #ListLevelVM[listX.index(min(listX))]
        EST = min(listESTVM[vmn])
        taskcore = listESTVM[vmn].index(EST)   

        return vmn,taskcore,EST

def getEST_EFT(self):
    NumPre = len(self.inputs)  #父节点的个数
    NumSuc = len(self.outputs) #子节点的个数  
    vmn = None                 #将要选择的VM
    taskcore = None            #将要选择的VM的核      
    EFT = 0                 #最早开始时间
    listInputs = self.inputs
    # if NumPre>0:
    '''
    包含父节点的task，先计算最早可开始时间（所有父节点最晚的完工时间、相应的父节点）和对应的VM、父节点所在VM的完工时间
    最早可开始时间（Earliest Start Time, EST）      EST_VM(当跨VM时需要传输时间)
    父节点所在VM的完工时间

    在计算当前节点的开始时间时，要加上父节点的传输时间
    '''   
    VMNums = len(VMS)                
    listESTVM = []
    for j in range(VMNums):                     #listESTVM[j][k] 第j台VM的第k个核上的EST,最后在此列表中取最小的VM、核
        listESTVM.append([])
        for k in range(VMS[j].NumCores):
            listESTVM[j].append(VMS[j].CompleteTime[k])

    listEST = [[] for j in range(2)]            #0 = id (task)   1 = Finishtime     
    for j in range(NumPre):
        listEST[0].append(listInputs[j].id)
        listEST[1].append(SimplifiedWorkflow[listInputs[j].id].FinishTime)

        for j1 in range(VMNums):
            DataTransferRate = None
            if j1 == SimplifiedWorkflow[listEST[0][j]].VMnum:
                DataTransferRate = 0
            # elif   j1 < SimplifiedWorkflow[listEST[0][j]].VMnum:   ###     20210923更改
            elif   VMS[j1].id <= VMS[SimplifiedWorkflow[listEST[0][j]].VMnum].id:
                DataTransferRate = VMT.B[VMS[j1].id]
            else:
                DataTransferRate = VMT.B[VMS[ SimplifiedWorkflow[listEST[0][j]].VMnum].id]
            
            DataTransferTime = 0 if DataTransferRate == 0 else (listInputs[j].size/DataTransferRate * DTT)  #将传输时间放大DTT倍 
            
            startTimePreDTT = listEST[1][j]+DataTransferTime
            for k in range(VMS[j1].NumCores):
                listESTVM[j1][k] = max(listESTVM[j1][k],startTimePreDTT) #,VMS[j1].CompleteTime[k]
    
    for j in range(VMNums):  
        for k in range(VMS[j].NumCores):    
            listESTVM[j][k] += (self.runtime/VMT.ProcessingCapacity[VMS[j].id])

    listX = [ min(listESTVM[j]) for j in range(VMNums)] 
    # EFT = min(listX) 

    listX0 = [ round(min(listESTVM[j]),3) for j in range(VMNums)]
    EFT0 = min(listX0)


    if listX0.count(EFT0)>1:
        Difference = []
        for i in range(VMNums):
            if listX0[i]==EFT0:
                Difference.append([i,listX0[i]-min(VMS[i].CompleteTime)]) #[[i,listX[i]-min(VMS[i].CompleteTime)] for i in range(VMNums)  ]
        Dif = sorted(Difference, key=lambda Difference: Difference[1])
        vmn = Dif[0][0] #listX.index(min(listX))            
        for i1 in range(1,len(Dif)):
            if (Dif[i1][1] == Dif[0][1]) and (VMS[vmn].id<VMS[Dif[i1][0]].id):# 3): #and(vmn<Dif[0][0]+3): #GlobalResource.SuitVM):# 
                vmn = Dif[i1][0]
                break
    else :
        vmn = listX.index(min(listX))

    # vmn = listX.index(min(listX))
    EFT = min(listESTVM[vmn])
    taskcore = listESTVM[vmn].index(EFT)
         
    EST = EFT-(self.runtime/VMT.ProcessingCapacity[VMS[vmn].id])
    return vmn,taskcore,EST


def CalcaulateTaskObject(taskID,vmn,taskcore,EST):

    # vmn,taskcore,EST = getEST(SimplifiedWorkflow[taskID])

    SimplifiedWorkflow[taskID].VMnum = vmn  
    #待定，需要修改                
    SimplifiedWorkflow[taskID].VMcore = taskcore        
        
    #开始执行时间待定，需要修改   '空格\' 为换行符
    SimplifiedWorkflow[taskID].StartTime = EST           # min(VMS[vmn].CompleteTime)
    SimplifiedWorkflow[taskID].FinishTime = EST + (SimplifiedWorkflow[taskID].runtime
                                                        /VMT.ProcessingCapacity[VMS[vmn].id])
    
    VMS[vmn].CompleteTime[taskcore] = SimplifiedWorkflow[taskID].FinishTime
    VMS[vmn].TaskCore[taskcore].insert(len(VMS[vmn].TaskCore[taskcore]),taskID)
    
    list1 = list([SimplifiedWorkflow[taskID].StartTime,SimplifiedWorkflow[taskID].FinishTime])
    VMS[vmn].VMTime[taskcore].insert(len(VMS[vmn].VMTime[taskcore]),list1)

def gantt(self):
    """甘特图
    m机器集
    t时间集
    plt.barh(y,data,left=())  y是条形图的位置，data是条形图的大小，left是条形图坐标的距离。
    plt.barh(y, width, left, edgecolor, color)

    y 参数表示y轴坐标

    width 表示矩形块的长度，也就是任务加工时间，任务持续时间等参数

    left 表示矩形块最左边的 x轴坐标，

    这样就能确定一个矩形块在图中的位置

    edgecolor 表示矩形块的边的颜色，通常设置为 black

    color 表示矩形块的颜色
    plt.text(x, y, label, font_style)
    x 表示x轴坐标
    y 表示y轴坐标
    label 表示要添加的标签内容
    font_style 标签字体的风格

    6）plt.annotate(s, xy, xytext) # 添加注释，除s、xy外其余还有若干可选参数。

    s：注释文本，

    xy：指定要注释的（x，y）坐标点，

    xytext：可选，指定要放置文本的（x，y）坐标点。如果没有，则默认为xy注释点。

    arrowprops：可选，字典形式，用于在xy坐标和xytext间绘制一个指定形状的箭头，本例中指定一个'->'类型的箭头，箭头头部宽和高为0.2/0.4。

    7）plt.quiver(X, Y, U, V, C, **kw) # 绘制一个二维的箭头，X, Y, C可以缺失。

    X, Y：箭头的位置，

    U, V：表示箭头的方向，

    C：设置箭头的颜色，

    **kw里还有一系列参数可以设置，包括单位、箭头角度、箭头的头部宽高设置等，这里设置了颜色color和箭头的轴宽度width。    
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']#解决中文显示为方框的问题  "|","+",
    colors = ['red', 'orange', 'gold', 'lawngreen', 'lightseagreen', 'royalblue','blueviolet']
    # colors = ['dimgray','tan','lightblue','coral','g','r','silver','y','c']
    marks = ["","\\","/","X","+",".","*","o"]
    #画布设置，大小与分辨率
    plt.figure(figsize=(20,8),dpi=80)
    #barh-柱状图换向，循坏迭代-层叠效果
    listY = []
    strY = []
    yHeigh = 0
    VMNums = len(self)
    for VMnumID in range(VMNums):                               #VM层
        ProcessingTasks = False
        for TaskCoreID in range(self[VMnumID].NumCores):
            if len(self[VMnumID].TaskCore[TaskCoreID])>0:
               ProcessingTasks = True
               break 
        if ProcessingTasks:    
            plt.axhline(y=yHeigh+0.6, c="r", ls="--", lw=2)  
            for TaskCoreID in range(self[VMnumID].NumCores) :        #VM的核层
                if len(self[VMnumID].TaskCore[TaskCoreID])>0:
                    yHeigh = yHeigh + 1
                    listY.insert(len(listY), yHeigh)
                    strY.insert(len(strY),'VM%s_%s_%s'%(VMnumID,self[VMnumID].NumCores,self[VMnumID].id)) #TaskCoreID
                for taskID in range(len(self[VMnumID].TaskCore[TaskCoreID])):
                    task = self[VMnumID].TaskCore[TaskCoreID][taskID]
                    # self[VMnumID].VMTime[taskID][0]  #开始时间  
                    # self[VMnumID].VMTime[taskID][1]  #结束时间
                    strTask = SimplifiedWorkflow[task].jobsetname if SimplifiedWorkflow[task].jobsetname else task
                    
                    plt.barh(yHeigh,left=self[VMnumID].VMTime[TaskCoreID][taskID][0],
                        width=self[VMnumID].VMTime[TaskCoreID][taskID][1]-self[VMnumID].VMTime[TaskCoreID][taskID][0],
                        height=0.6,hatch = marks[SimplifiedWorkflow[task].Level % len(marks)],#)
                        color =colors[SimplifiedWorkflow[task].Level % len(colors)],
                        edgecolor="k")  ##'w' 
                        
                    plt.text(self[VMnumID].VMTime[TaskCoreID][taskID][0]+
                        (self[VMnumID].VMTime[TaskCoreID][taskID][1]-
                        self[VMnumID].VMTime[TaskCoreID][taskID][0])/3,
                        yHeigh+0.35,'T%s'%(strTask),color="k") #     ,size=8)

    plt.axhline(y=yHeigh + 0.8, c="r", ls="--", lw=2)

    Cmax = 0
    CmaxVm = None
    CmaxCore = None 
    y3 = 0
    for task,task1 in SimplifiedWorkflow.items(): 
        '''
        绘制含传输时间的边
        '''  
        if Cmax<task1.FinishTime:
            Cmax = task1.FinishTime
            CmaxVm = SimplifiedWorkflow[task].VMnum
            CmaxCore = self[CmaxVm].id  #SimplifiedWorkflow[task].VMcore
            y3 = listY[strY.index('VM%s_%s_%s'%(CmaxVm,self[CmaxVm].NumCores,CmaxCore))]

        VMnumID = SimplifiedWorkflow[task].VMnum 
        for each in SimplifiedWorkflow[task].inputs:
            if (SimplifiedWorkflow[each.id].VMnum != VMnumID):
                i = SimplifiedWorkflow[each.id].VMnum
                j = self[i].NumCores
                k = self[i].id  #SimplifiedWorkflow[each.id].VMcore
                y1 = listY[strY.index('VM%s_%s_%s'%(i,j,k))]
                
                j = self[VMnumID].NumCores
                k = self[VMnumID].id  #SimplifiedWorkflow[task].VMcore
                y2 = listY[strY.index('VM%s_%s_%s'%(VMnumID,j,k))]     # '%s'(   ) str(task)      

                plt.annotate('',xytext=(SimplifiedWorkflow[each.id].FinishTime ,y1),
                    xy= (SimplifiedWorkflow[task].StartTime ,y2),
                    arrowprops=dict(arrowstyle="->") )
                    
    plt.annotate('Cmax = %.2f'%Cmax,xy=(Cmax,y3),xytext= (Cmax*0.98 ,y3+1),c = 'r',
                    arrowprops=dict(arrowstyle="->") )
                     
    plt.yticks(listY,strY)
    # plt.title("WorkflowScheduling_%s_%s"%(GlobalResource.WorkFlowTestName,os.path.basename(__file__).split(".")[0]))
    plt.title("WorkflowScheduling_%s_%s_%s"%(WorkFlowTestName,DeadlineFactor,os.path.basename(__file__).split(".")[0]))
    # plt.legend(handles=patches,loc=4)
    #XY轴标签
    plt.xlabel("Time/s")
    plt.ylabel("VM")    
    #plt.grid(linestyle="--",alpha=0.5)  #网格线
    plt.savefig(".\GanttChart\WorkflowScheduling_%s_%s_%s1.png"%(WorkFlowTestName,DeadlineFactor,
        os.path.basename(__file__).split(".")[0]), dpi=300, format='png',bbox_inches="tight")
    # plt.show()     gantt_VMState(VMS)

def gantt_VMState(self):
    plt.rcParams['font.sans-serif'] = ['SimHei']#解决中文显示为方框的问题  "|","+",
    colors = ['red', 'orange', 'gold', 'lawngreen', 'lightseagreen', 'royalblue','blueviolet']
    # colors = ['dimgray','tan','lightblue','coral','g','r','silver','y','c']
    marks = ["","\\","/","X","+",".","*","o"]
    #画布设置，大小与分辨率
    plt.figure(figsize=(20,8),dpi=80)
    #barh-柱状图换向，循坏迭代-层叠效果
    listY = []
    strY = []
    yHeigh = 0
    BarHeight = 0.6
    LineWidth = 0.5
    FontSize = 15
    VMNums = len(self)
    Number_VM = 0
    for VMnumID in range(VMNums):                               #VM层
        ProcessingTasks = False
        for TaskCoreID in range(self[VMnumID].NumCores):
            if len(self[VMnumID].TaskCore[TaskCoreID])>0:
               ProcessingTasks = True
               break 
        if ProcessingTasks:    
            plt.axhline(y=yHeigh+BarHeight, c="r", ls="--", lw=LineWidth)  
            for TaskCoreID in range(self[VMnumID].NumCores) :        #VM的核层
                if len(self[VMnumID].TaskCore[TaskCoreID])>0:
                    yHeigh = yHeigh + 1
                    listY.insert(len(listY), yHeigh)
                    strY.insert(len(strY),'VM%s_%s'%(VMnumID,self[VMnumID].id)) #TaskCoreID
                    plt.barh(yHeigh,left=self[VMnumID].VMTime[TaskCoreID][0][0],#label='Booting',
                        width=GlobalResource.AWSCOLDSTARTUP,
                        height=BarHeight, #hatch = marks[SimplifiedWorkflow[task].Level % len(marks)],#)
                        color = "k", # colors[SimplifiedWorkflow[task].Level % len(colors)],
                        edgecolor="k")  ##'w'
                    # plt.text(self[VMnumID].VMTime[TaskCoreID][0][0],
                    #     yHeigh+0.35,color="k",fontsize = FontSize-2) # ,'Booting'    ,size=8)                     
                for taskID in range(len(self[VMnumID].TaskCore[TaskCoreID])):
                    task = self[VMnumID].TaskCore[TaskCoreID][taskID]
                    # self[VMnumID].VMTime[taskID][0]  #开始时间  
                    # self[VMnumID].VMTime[taskID][1]  #结束时间
                    strTask1 = SimplifiedWorkflow[task].jobsetname if SimplifiedWorkflow[task].jobsetname else task
                    strTask = '' #'str()'
                    for numbers in strTask1:
                        if numbers.isdigit():
                            strTask += str(int(numbers)+1)
                            # strTask.replace(numbers,str(int(numbers)+1))
                        else:
                            strTask = strTask+'\\'+numbers

                    plt.barh(yHeigh,left=self[VMnumID].VMTime[TaskCoreID][taskID][0] +GlobalResource.AWSCOLDSTARTUP,
                        width=self[VMnumID].VMTime[TaskCoreID][taskID][1]-self[VMnumID].VMTime[TaskCoreID][taskID][0],
                        height=BarHeight,hatch = marks[SimplifiedWorkflow[task].Level % len(marks)],#)
                        color =colors[SimplifiedWorkflow[task].Level % len(colors)],
                        edgecolor="k")  ##'w' 
                        
                    plt.text(self[VMnumID].VMTime[TaskCoreID][taskID][0]+
                        (self[VMnumID].VMTime[TaskCoreID][taskID][1]-
                        self[VMnumID].VMTime[TaskCoreID][taskID][0])/3 +GlobalResource.AWSCOLDSTARTUP,
                        yHeigh+0.35,'$T_{%s}$'%(strTask),color="k",fontsize = FontSize-2) #     ,size=8)

                    if  (taskID>0) and(  self[VMnumID].VMTime[TaskCoreID][taskID][0]-self[VMnumID].VMTime[TaskCoreID][taskID-1][1]> GlobalResource.HibernateLowerBound ):   
                        ###   Hibernate
                        startime1 = self[VMnumID].VMTime[TaskCoreID][taskID-1][1] +GlobalResource.AWSCOLDSTARTUP
                        Totalwidth = self[VMnumID].VMTime[TaskCoreID][taskID][0]-self[VMnumID].VMTime[TaskCoreID][taskID-1][1]
                        width1 = Totalwidth - GlobalResource.AWSWARMSTARTUP

                        plt.barh(yHeigh,left=startime1,#label='Hibernate',
                            width=width1,
                            height=BarHeight, # hatch = marks[SimplifiedWorkflow[task].Level % len(marks)],#)
                            color = 'dimgray', # colors[SimplifiedWorkflow[task].Level % len(colors)],
                            edgecolor="k")  ##'w' 

                        # plt.text(startime1+(width1)/3,yHeigh+0.35,color="k",fontsize = FontSize-2) # 'Hibernate',    ,size=8)
                        
                        ###   Booting
                        startime2 = startime1 + width1
                        width2 = GlobalResource.AWSWARMSTARTUP
                        plt.barh(yHeigh,left=startime2,width=width2,#label='Booting',
                            height=BarHeight, # hatch = marks[SimplifiedWorkflow[task].Level % len(marks)],#)
                            color = 'k', # colors[SimplifiedWorkflow[task].Level % len(colors)],
                            edgecolor="k")  ##'w' 

                        # plt.text(startime2,yHeigh+0.35,color="k",fontsize = FontSize-2) #  'Booting',   ,size=8)                        

    plt.axhline(y=yHeigh + BarHeight, c="r", ls="--", lw=LineWidth)
    plt.barh(y=yHeigh,width=0,label='Booting',color = "k",edgecolor="k")
    plt.barh(y=yHeigh,width=0,label='Hibernate',color = "dimgray",edgecolor="k")
    plt.legend()
            # ('Hibernate','Booting')loc ='lower center',frameon=False,ncol=4,bbox_to_anchor=(0.5,0.9),fontsize=10,handlelength=2.5)
    Cmax = 0
    CmaxVm = None
    CmaxCore = None 
    y3 = 0
    for task,task1 in SimplifiedWorkflow.items(): 
        '''
        绘制含传输时间的边
        '''  
        if Cmax<task1.FinishTime:
            Cmax = task1.FinishTime
            CmaxVm = SimplifiedWorkflow[task].VMnum
            CmaxCore = self[CmaxVm].id  #SimplifiedWorkflow[task].VMcore
            y3 = listY[strY.index('VM%s_%s'%(CmaxVm,CmaxCore))]

        VMnumID = SimplifiedWorkflow[task].VMnum 
        for each in SimplifiedWorkflow[task].inputs:
            if (SimplifiedWorkflow[each.id].VMnum != VMnumID):
                i = SimplifiedWorkflow[each.id].VMnum
                j = self[i].NumCores
                k = self[i].id  #SimplifiedWorkflow[each.id].VMcore
                y1 = listY[strY.index('VM%s_%s'%(i,k))]
                
                j = self[VMnumID].NumCores
                k = self[VMnumID].id  #SimplifiedWorkflow[task].VMcore
                y2 = listY[strY.index('VM%s_%s'%(VMnumID,k))]     # '%s'(   ) str(task)      

                plt.annotate('',xytext=(SimplifiedWorkflow[each.id].FinishTime +GlobalResource.AWSCOLDSTARTUP ,y1),
                    xy= (SimplifiedWorkflow[task].StartTime +GlobalResource.AWSCOLDSTARTUP ,y2),
                    arrowprops=dict(arrowstyle="->") )
                    
    # plt.annotate('Cmax = %.2f'%Cmax,xy=(Cmax,y3),xytext= (Cmax*0.98 ,y3+1),c = 'r',
    #                 arrowprops=dict(arrowstyle="->") )
    # subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    strY = ['$I_'+str(i)+'$'+'($P_'+strY[i][-1:]+'$)'for i in range(len(listY))]                 
    plt.yticks(listY,strY,fontsize = FontSize)
    plt.xticks(fontsize = FontSize)
    # plt.title("WorkflowScheduling_%s_%s"%(GlobalResource.WorkFlowTestName,os.path.basename(__file__).split(".")[0]))
    # plt.title("WorkflowScheduling_%s_%s_%s"%(WorkFlowTestName,DeadlineFactor,os.path.basename(__file__).split(".")[0]))
    # plt.legend(handles=patches,loc=4)
    #XY轴标签
    plt.xlabel("Time/s",fontsize = FontSize)
    plt.ylabel("VM",fontsize = FontSize)    
    #plt.grid(linestyle="--",alpha=0.5)  #网格线
    plt.savefig(".\GanttChart\WorkflowScheduling_%s_%s_%s1.png"%(WorkFlowTestName,DeadlineFactor,
        os.path.basename(__file__).split(".")[0]), dpi=300, format='png',bbox_inches="tight")
    plt.show()    # gantt_VMState(VMS)

############ 2021 09 23   ######################################################################
def Adaptively_Adjust_First_Task_Block():
    global VMS,SimplifiedWorkflow
    VMNums = len(VMS)
    while True:
        no_find_Block = True
        for VMnumID in range(VMNums):                                       #VM 
            for TaskCoreID in range(VMS[VMnumID].NumCores):                 #对应的核                
                if len(VMS[VMnumID].TaskCore[TaskCoreID]) > 0:              #任务个数大于1
                    tasklist = [VMS[VMnumID].TaskCore[TaskCoreID][0]]
                    for t_i in range(1,len(VMS[VMnumID].TaskCore[TaskCoreID])):    #逐个任务
                        if VMS[VMnumID].VMTime[TaskCoreID][t_i-1][1] == VMS[VMnumID].VMTime[TaskCoreID][t_i][0]:
                            # 上一个任务的完成时间  == 当前任务的开始时间
                            tasklist.append(VMS[VMnumID].TaskCore[TaskCoreID][t_i])#insert(len(tasklist),VMS[VMnumID].TaskCore[TaskCoreID][t_i])
                        else:
                            break
                    # if True: #len(tasklist)<len(VMS[VMnumID].TaskCore[TaskCoreID]):
                        
                    # DelayTime = min{LFT,AFT} 延迟的时间
                    # LFT :最晚完成时间，每个子任务的开始时间减去与该任务的传输时间  AFT：实际完成时间
                    # TransTime:传输时间
                    LFT = []
                    AFT = []
                    for each in tasklist:                            
                        list_AST_TransT = []   #AST减去 传输时间
                        if SimplifiedWorkflow[each].outputs == []:
                            list_AST_TransT.append(SimplifiedWorkflow[each].FinishTime)   # AFT # (Deadline)
                        else:
                            for child in SimplifiedWorkflow[each].outputs:
                                if  not(child.id in tasklist):
                                    AST_child = SimplifiedWorkflow[child.id].StartTime
                                    # TransTime =
                                    DataTransferRate = None
                                    if VMnumID == SimplifiedWorkflow[child.id].VMnum:
                                        DataTransferRate = 0
                                    elif   VMS[VMnumID].id <= VMS[SimplifiedWorkflow[child.id].VMnum].id:
                                        DataTransferRate = VMT.B[VMS[VMnumID].id]
                                    else:
                                        DataTransferRate = VMT.B[VMS[SimplifiedWorkflow[child.id].VMnum].id]                                
                                    TransTime = 0 if DataTransferRate == 0 else (child.size/DataTransferRate * DTT)  #将传输时间放大DTT倍
                                    list_AST_TransT.append(AST_child-TransTime)
                        if list_AST_TransT != []:        
                            LFT.append(min(list_AST_TransT))
                            AFT.append(SimplifiedWorkflow[each].FinishTime)
                    if LFT != []:         
                        LFT_AFT = list(map(lambda x: x[0]-x[1], zip(LFT, AFT)))  #if LFT != []: 
                        if len(tasklist)<len(VMS[VMnumID].TaskCore[TaskCoreID]):
                            LFT_AFT.append( VMS[VMnumID].VMTime[TaskCoreID][len(tasklist)][0]-VMS[VMnumID].VMTime[TaskCoreID][len(tasklist)-1][1] )
                        if min(LFT_AFT)>0:
                            no_find_Block = False
                            for i in range(len(tasklist)):
                                SimplifiedWorkflow[tasklist[i]].FinishTime += min(LFT_AFT)
                                SimplifiedWorkflow[tasklist[i]].StartTime  += min(LFT_AFT)
                                VMS[VMnumID].VMTime[TaskCoreID][i][0] += min(LFT_AFT)
                                VMS[VMnumID].VMTime[TaskCoreID][i][1] += min(LFT_AFT)

        if no_find_Block: break
    # return VMS,SimplifiedWorkflow

############ 2021 10 13   ######################################################################
def BlockTime_IdleTime_Sort(): 
    tasklist_VM_Core = []
    for VMnumID in range(VMNums):                                       #VM 
        for TaskCoreID in range(VMS[VMnumID].NumCores):                 #对应的核                
            if len(VMS[VMnumID].TaskCore[TaskCoreID]) > 1:              #任务个数大于1
                tasklist = [VMS[VMnumID].TaskCore[TaskCoreID][len(VMS[VMnumID].TaskCore[TaskCoreID])-1]]
                for t_i in range(len(VMS[VMnumID].TaskCore[TaskCoreID])-2,-1,-1):    #逐个任务
                    if VMS[VMnumID].VMTime[TaskCoreID][t_i][1] == VMS[VMnumID].VMTime[TaskCoreID][t_i+1][0]:
                        # 当前任务的完成时间  == 下一个任务的开始时间
                        tasklist.append(VMS[VMnumID].TaskCore[TaskCoreID][t_i])#insert(len(tasklist),VMS[VMnumID].TaskCore[TaskCoreID][t_i])
                    else:
                        break
                if len(tasklist)<len(VMS[VMnumID].TaskCore[TaskCoreID]):  
                    tasklist_VM_Core.insert(len(tasklist_VM_Core),[(VMnumID,TaskCoreID)])   # (Vm_num,Core_num)
                    tasklist_VM_Core[len(tasklist_VM_Core)-1].append(tasklist)              # [块结构的任务]
                    BlockTime = VMS[VMnumID].VMTime[TaskCoreID][len(VMS[VMnumID].TaskCore[TaskCoreID])-1][1]- VMS[VMnumID].VMTime[TaskCoreID][t_i+1][0]
                    IdleTime = VMS[VMnumID].VMTime[TaskCoreID][t_i+1][0] - VMS[VMnumID].VMTime[TaskCoreID][t_i][1]
                    tasklist_VM_Core[len(tasklist_VM_Core)-1].append([(BlockTime,IdleTime),BlockTime/IdleTime]) 
    return sorted(tasklist_VM_Core, key=lambda tasklist_VM_Core: tasklist_VM_Core[2][1])    # tasklist_VM_Core_sort =

def TaskScheduling_Blocks(BTIS):
    NumBlock = 2
    TaskList = []
    Block_VM = []
    for i in range(NumBlock):
        Block_VM.append(BTIS[i][0][0])
        for j in BTIS[i][1]:
            TaskList.append(j)
    VM_set = []
    for VMnumID in range(VMNums):
        if max(VMS[VMnumID].CompleteTime)>0:
            VM_set.append(VMnumID)
    VM_set = list(set(VM_set) - set(Block_VM))   

    k = TaskList[0]
    j = k

###########################################################################
###########################################################################
###########################################################################
def gantt_VMState_MultiWorkflow(self,multiWorflow,objectives):
    global PUBLICID,PRIVATEID
    # font = FontProperties()
    # font.set_name('Times New Roman')
    # path = '/path/to/custom/font.ttf'
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']#解决中文显示为方框的问题  "|","+",
    # myfont=fm.FontProperties(fname=".\\Class\\times.ttf")
    plt.rcParams["font.family"] = "times new roman"
    colorNum = 10
    cmap = plt.get_cmap('gist_rainbow',colorNum) #  spring  Paired autumn
    colors = cmap(np.linspace(0,1,colorNum))
    # ['red', 'royalblue', 'gold', 'lawngreen', 'orange', 'blueviolet']
    # colors = ['dimgray','tan','lightblue','coral','g','r','silver','y','c']'lightseagreen',
    marks = ["","\\","/","X","+",".","*","o"]
    #画布设置，大小与分辨率
    plt.figure(dpi=85)
    #barh-柱状图换向，循坏迭代-层叠效果figsize=(20,8),
    listY = []
    strY = []
    yHeigh = -0.15
    BarHeight = 0.5
    LineWidth = 0.5
    LW2 =0.15
    FontSize = 11
    # VMNums = len(self)
    edgecolor = "w"#silver"
    Number_VM = 0
    taskVMHeigh = {}
    for CloudID in HYBRIDCLOUD:
        VMNums = len(self[CloudID])
        num = 0
        plt.axhline(y=yHeigh + BarHeight*0.6, c="r", ls="-", lw=LineWidth*1.5)    
        for VMnumID in range(VMNums):                               #VM层
            ProcessingTasks = False
            for TaskCoreID in range(self[CloudID][VMnumID].NumCores):
                if len(self[CloudID][VMnumID].TaskCore[TaskCoreID])>0:
                    ProcessingTasks = True
                    break 
            if ProcessingTasks:    
                # plt.axhline(y=yHeigh+BarHeight*0.6, c="r", ls="--", lw=LineWidth)  
                for TaskCoreID in range(self[CloudID][VMnumID].NumCores) :        #VM的核层
                    if len(self[CloudID][VMnumID].TaskCore[TaskCoreID])>0:
                        num += 1
                        yHeigh = yHeigh + BarHeight*1.2
                        listY.insert(len(listY), yHeigh)
                        strY.insert(len(strY),'VM%s_%s_%s'%(CloudID,num,self[CloudID][VMnumID].id)) #TaskCoreID
                        if CloudID==PRIVATEID:
                            plt.barh(yHeigh,left=0,#label='Booting',
                                width=GlobalResource.AWSCOLDSTARTUP,
                                height=BarHeight, #hatch = marks[SimplifiedWorkflow[task].Level % len(marks)],#)
                                color = "k")#, # colors[SimplifiedWorkflow[task].Level % len(colors)],
                                # edgecolor=edgecolor)  ##'w'
                            # plt.text(self[VMnumID].VMTime[TaskCoreID][0][0],
                            #     yHeigh+0.35,color="k",fontsize = FontSize-2) # ,'Booting'    ,size=8)       
                        else:
                            plt.barh(yHeigh,left=self[CloudID][VMnumID].VMTime[TaskCoreID][0][0],#label='Booting',
                                width=GlobalResource.AWSCOLDSTARTUP,
                                height=BarHeight, #hatch = marks[SimplifiedWorkflow[task].Level % len(marks)],#)
                                color = "k")#, # colors[SimplifiedWorkflow[task].Level % len(colors)],
                                # edgecolor=edgecolor)  ##'w'
                            # plt.text(self[VMnumID].VMTime[TaskCoreID][0][0],
                            #     yHeigh+0.35,color="k",fontsize = FontSize-2) # ,'Booting'    ,size=8)                     
                    for taskID in range(len(self[CloudID][VMnumID].TaskCore[TaskCoreID])):
                        wNum = self[CloudID][VMnumID].TaskCore[TaskCoreID][taskID][0]
                        task = self[CloudID][VMnumID].TaskCore[TaskCoreID][taskID][1]
                        # self[VMnumID].VMTime[taskID][0]  #开始时间  
                        # self[VMnumID].VMTime[taskID][1]  #结束时间
                        taskVMHeigh[str(wNum)+'_'+str(task)] = yHeigh
                        strTask = '' #'str()'    
                        if multiWorflow[wNum][task].jobsetname:
                            strTask1 = multiWorflow[wNum][task].jobsetname
                            str1 = ''                        
                            for numbers in str(strTask1):
                                if numbers.isdigit():
                                    str1 += numbers
                                else:
                                    strTask += (str(int(str1)+1) +'\\'+numbers)
                                    str1 = '' # str1+'\\'+numbers
                            strTask += str(int(str1)+1)
                        else:
                            strTask = str(task+1)
                        if multiWorflow[wNum][task].MI==1:
                            plt.barh(yHeigh,left=self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0] +GlobalResource.AWSCOLDSTARTUP,
                                width=self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]-self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0],
                                height=BarHeight,  hatch ="//",
                                color ='w',linewidth=LW2*4, 
                                edgecolor='darkorange')  ##'w' fontproperties=myfont,
                        else:
                            plt.barh(yHeigh,left=self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0] +GlobalResource.AWSCOLDSTARTUP,
                                width=self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]-self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0],
                                height=BarHeight, # hatch = marks[multiWorflow[wNum][task].Level % len(marks)],#)
                                color =colors[multiWorflow[wNum][task].Level % len(colors)],linewidth=LW2,
                                edgecolor=edgecolor)  ##'w' fontproperties=myfont,
                            
                        plt.text(self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]+GlobalResource.AWSCOLDSTARTUP
                            +(self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]-self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0])/3
                            ,yHeigh-0.1,'a'+r'$^{%s}_{%s}$'%(str(wNum),strTask),color="k",size=FontSize, # yHeigh+0.2,'a'+r'$_{%s}$'%(strTask),color="k",size=FontSize-2,
                            family='serif', style='italic'
                            ) # *0.98 fontdict={"family":'times','size':FontSize-2} family="Times new roman",fontsize = FontSize-2    ,size=8)

                        ### 绘制休眠
                        if CloudID==0:
                            if  (taskID>0) and(  self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]-self[CloudID][VMnumID].VMTime[TaskCoreID][taskID-1][1]> GlobalResource.HibernateLowerBound ):   
                                ###   Hibernate
                                startime1 = self[CloudID][VMnumID].VMTime[TaskCoreID][taskID-1][1] +GlobalResource.AWSCOLDSTARTUP
                                Totalwidth = self[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]-self[CloudID][VMnumID].VMTime[TaskCoreID][taskID-1][1]
                                width1 = Totalwidth - GlobalResource.AWSWARMSTARTUP

                                plt.barh(yHeigh,left=startime1,#label='Hibernate',
                                    width=width1,
                                    height=BarHeight,linewidth=LW2, # hatch = marks[multiWorflow[wNum][task].Level % len(marks)],#)
                                    color = 'dimgray') #, colors[multiWorflow[wNum][task].Level % len(colors)],
                                    #edgecolor=edgecolor  #'w' )#

                                # plt.text(startime1+(width1)/3,yHeigh+0.35,color="k",fontsize = FontSize-2) # 'Hibernate',    ,size=8)
                                
                                ###   Booting
                                startime2 = startime1 + width1
                                width2 = GlobalResource.AWSWARMSTARTUP
                                plt.barh(yHeigh,left=startime2,width=width2,#label='Booting',
                                    height=BarHeight,linewidth=LW2, # hatch = marks[multiWorflow[wNum][task].Level % len(marks)],#)
                                    color = 'k')#, # colors[multiWorflow[wNum][task].Level % len(colors)],
                                    # edgecolor=edgecolor)  ##'w' 

                                # plt.text(startime2,yHeigh+0.35,color="k",fontsize = FontSize-2) #  'Booting',   ,size=8)                        
                plt.axhline(y=yHeigh+BarHeight*0.6, c="darkgray", ls="--", lw=LineWidth) 
    plt.axhline(y=yHeigh + BarHeight*0.6, c="r", ls="-", lw=LineWidth*1.5)            
    # plt.axhline(y=yHeigh + BarHeight*0.6, c="r", ls="--", lw=LineWidth)
    plt.barh(y=yHeigh*0.75,width=0,label='Booting',color = "k")#,edgecolor=edgecolor)
    plt.barh(y=yHeigh*0.75,width=0,label='Hibernate',color = "dimgray")#,edgecolor=edgecolor)
    plt.legend(prop={'size': FontSize-3},borderpad=0.1,labelspacing=0.1)
            # ('Hibernate','Booting')loc ='lower center',frameon=False,ncol=4,bbox_to_anchor=(0.5,0.9),fontsize=10,handlelength=2.5)

    # taskVMHeigh[str(wNum)+'_'+str(task)]
    for i in range(len(multiWorflow)):
        for taskID,task in multiWorflow[i].items(): 
            '''
            绘制含传输时间的边
            '''  
            VMnumID = task.VMnum 
            for parent in task.inputs:
                parentVMID = multiWorflow[i][parent.id].VMnum 
                if VMnumID[0]==PRIVATEID or  parentVMID[0]==PRIVATEID:
                    ytask = taskVMHeigh[str(i)+'_'+str(task.id)]
                    yparent = taskVMHeigh[str(i)+'_'+str(parent.id)]
                    if ytask!=yparent:
                        plt.annotate('',xytext=(multiWorflow[i][parent.id].FinishTime +GlobalResource.AWSCOLDSTARTUP ,yparent),
                            xy= (task.StartTime +GlobalResource.AWSCOLDSTARTUP ,ytask),color="b",
                            arrowprops=dict(arrowstyle="->,head_length=0.2,head_width=0.2",lw=LW2) )


    # plt.annotate('Cmax = %.2f'%Cmax,xy=(Cmax,y3),xytext= (Cmax*0.98 ,y3+1),c = 'r',
    #                 arrowprops=dict(arrowstyle="->") )
    # subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")+'\n'
    listY1 = [re.findall(r"\d+\.?\d*",i) for i in strY]
    strY = ['$v^{'+str(i[0])+'}_{'+str(i[1])+'}$($p_{'+i[2]+'}$)'for i in listY1]   

    plt.yticks(listY,strY,family='Times new roman',fontsize = FontSize)
    plt.xticks(fontsize = FontSize)
    plt.title("WorkflowScheduling_%s_%.3f_%.3f_%.3f_%.3f"%(WorkFlowTestName, #GlobalResource. _%s os.path.basename(__file__).split(".")[0],
                                        objectives.Cmax,objectives.Cost,objectives.Energy,objectives.TotalTardiness))
    # plt.title("WorkflowScheduling_%s_%s_%s"%(WorkFlowTestName,DeadlineFactor,os.path.basename(__file__).split(".")[0]))
    # plt.legend(handles=patches,loc=4)
    #XY轴标签
    plt.xlabel("Time/s",fontsize = FontSize)
    plt.ylabel("VM",fontsize = FontSize)    
    #plt.grid(linestyle="--",alpha=0.5)  #网格线
    plt.savefig(".\GanttChart\WorkflowScheduling_%s_%s_%s.png"%(WorkFlowTestName,DeadlineFactor,
        os.path.basename(__file__).split(".")[0]), dpi=300, format='png',bbox_inches="tight")
    plt.show()    # gantt_VMState(VMS)

def case1_Private(self):
    '''
    Simplified DAG
    '''
    listNode = []
    setNode = set()
    for name,task in self.items():        
        tempName = name
        tempTask = task      
        tempList = set()  
        if not(tempName in setNode):            
            tempList = [tempName]
            while True:
                setNode.add(tempName)
                if (len(tempTask.outputs)==1)and(len(self[tempTask.outputs[0].id].inputs)==1)and(tempTask.MI== self[tempTask.outputs[0].id].MI):
                    tempList.append(tempTask.outputs[0].id)
                    tempName = tempTask.outputs[0].id
                    tempTask = self[tempTask.outputs[0].id]
                else:
                    break                 
                # if (len(tempTask.outputs)==1):
                #     if (len(self[tempTask.outputs[0].id].inputs)==1):
                #         tempList.append(tempTask.outputs[0].id)
                #         tempName = tempTask.outputs[0].id
                #         tempTask = self[tempTask.outputs[0].id] 
                #     else:
                #         break 
                # else:
                #     break 
        if len(tempList)>1: 
            listNode.insert(len(listNode),tempList) 
    for i in range(len(listNode)):
        self[listNode[i][0]].addjobsetname(str(listNode[i][0]))
        self[listNode[i][0]].outputs.pop()
        self[listNode[i][0]].outputs = self[listNode[i][len(listNode[i])-1]].outputs         
        for j in range(1,len(listNode[i])):
            self[listNode[i][0]].MI +=self[listNode[i][j]].MI
            self[listNode[i][0]].runtime +=self[listNode[i][j]].runtime 
            # self[listNode[i][0]].storage +=self[listNode[i][j]].storage
            if j == len(listNode[i])-1:
                for k in range(len(self[listNode[i][j]].outputs)):
                    for h in range(len(self[self[listNode[i][j]].outputs[k].id].inputs)):
                        if self[self[listNode[i][j]].outputs[k].id].inputs[h].id==listNode[i][j]:
                           self[self[listNode[i][j]].outputs[k].id].inputs[h].changeID(listNode[i][0]) 
            self[listNode[i][0]].addjobsetname(self[listNode[i][0]].jobsetname+'_'+str(listNode[i][j]))
            self.pop(listNode[i][j])    


    list1 = [i for i in range(len(self))]
    listkey = list(self.keys())
    for i in list1:
        if self[listkey[i]].jobsetname == None:
            self[listkey[i]].jobsetname = str(listkey[i])
        if i != listkey[i]:
            for parent in self[listkey[i]].inputs:
                for p_child in self[parent.id].outputs:
                    if p_child.id == listkey[i]:
                        p_child.id = i
            if self[listkey[i]].outputs != []:
                for child in self[listkey[i]].outputs:
                    for c_parent in self[child.id].inputs:
                        if c_parent.id == listkey[i]:
                            c_parent.id = i               
            self[listkey[i]].id = i 
            self[i] = self.pop(listkey[i])


def getMET_SubDeadline(workflow):
    MET = [0 for each in range(len(workflow))]  # {}#
    for taskid,task in workflow.items():
        MET[taskid] =task.runtime /GlobalResource.maxECU #math.trunc( )   
    return MET

def breadth_first_search_SubDeadline(workflow):#从前往后
    def bfs():
        while len(queue)> 0:
            node = queue.pop(0)
            booleanOrder[node] = True  
            for n in DAG[node].outputs:
                if (not n.id in booleanOrder) and (not n.id in queue):
                    queue.append(n.id)
                    order.append(n.id)     

    DAG = copy.deepcopy(workflow)
    DAG[len(DAG)] = Task(len(DAG),name = 'entry')
    list1 = [taskId for taskId,task in DAG.items()]
    for taskid in list1: #range(len(DAG)-1):
        if DAG[taskid].inputs == []:   #原源节点 size = 0  JITCAWorkflow[len(JITCAWorkflow)-1]
            tout = File('EntryOut', id = len(DAG)-1)
            DAG[taskid].inputs.append(tout)
            tout = File('Entry', id = taskid)
            DAG[len(DAG)-1].addOutput(tout)

    root = len(DAG)-1
    queue = []
    order = []
    booleanOrder = {}  
    queue.append(root)
    order.append(root)
    bfs()
    order.remove(order[0])
    return order

def getEST_SubDeadline(workflow,MET):
    scheduleOrder = breadth_first_search_SubDeadline(workflow)
    EST = [-1 for each in range(len(workflow))] # {} #
    EFT = [-1 for each in range(len(workflow))]  #{} #
    while True:
        if scheduleOrder == []:
            break    

        for taskid in scheduleOrder:
            parents = workflow[taskid].inputs
            if parents != []:
                boolean1 = False
                for each in parents:
                    if EST[each.id] == -1:
                        boolean1 = True
                        break
                if boolean1:
                    continue
                listPEST = [ EST[each.id] + MET[each.id] + each.size/GlobalResource.maxB for each in parents  ] #
                EST[taskid] = max(listPEST)
            else:
                EST[taskid] = 0
            EFT[taskid] = EST[taskid] + MET[taskid]
            scheduleOrder.remove(taskid)
            break
    return EST,EFT

def getLFT(workflow,MET,Deadline):
    scheduleOrder = breadth_first_search_SubDeadline(workflow)
    scheduleOrder.reverse()
    LFT = [-1 for each in range(len(workflow))]  #{} #
    LST = [-1 for each in range(len(workflow))]  #{} #
    while True:
        if scheduleOrder == []:
            break
        for taskid in scheduleOrder:
            child_1 = workflow[taskid].outputs
            if child_1 != []:
                boolean1 = False
                for each in child_1:
                    if LFT[each.id] == -1:
                        boolean1 = True
                        break
                if boolean1:
                    continue                    
                listCLFT = [ (LFT[each.id] - MET[each.id] - each.size/GlobalResource.maxB) for each in child_1  ]
                LFT[taskid] = min(listCLFT)
            else:
                LFT[taskid] = Deadline
            LST[taskid] = LFT[taskid] - MET[taskid]
            scheduleOrder.remove(taskid)
            break
    return LFT,LST

def getSubDeadline(workflow,Deadline):
    # ## subD_i = 
    # MET = getMET_SubDeadline(workflow)
    # EST,EFT = getEST_SubDeadline(workflow,MET)
    # SlackTime_maxEFT = 0.95*Deadline/max(EFT) # (1+(Deadline-max(EFT))/max(EFT) ) # 
    # for taskid,task in workflow.items():
    #     task.XFT = EFT[taskid] * SlackTime_maxEFT
    # # return workflow

    MET = getMET_SubDeadline(workflow)
    LFT,LST = getLFT(workflow,MET,Deadline)
    for taskid,task in workflow.items():
        if task.outputs ==[]:
            task.XFT = LFT[taskid]
        else:
            task.XFT = 0.95*LFT[taskid]  # # 对 sub-deadline 缩放
        task.LFT = LFT[taskid]

def ResetDeadline(workflow,DeadlineFactor):
    MET = getMET_SubDeadline(workflow)          #  /GlobalResource.maxECU
    EST,EFT = getEST_SubDeadline(workflow,MET)  #  /GlobalResource.maxB
    Deadline = max(EFT)*DeadlineFactor
    return Deadline



def Adaptively_Adjust_First_Task_Block_Multiworkflow(): 
    global VMS,multiWorflow  
    '''仅调整任务的开始和结束时间，结束时间设置为当前调度结果下的最晚结束时间''' 
    def AdjustListTasks():#tasklist,CloudID,VMnumID,TaskCoreID
        nonlocal no_find_Block
        # DelayTime = min{LFT,AFT} 延迟的时间
        # LFT :最晚完成时间，每个子任务的开始时间减去与该任务的传输时间  AFT：实际完成时间
        # TransTime:传输时间
        LFT = []
        AFT = []
        for each in tasklist:                            
            list_AST_TransT = []   #AST减去 传输时间
            if multiWorflow[each[0]][each[1]].outputs == []:
                list_AST_TransT.append(multiWorflow[each[0]][each[1]].FinishTime)   # AFT # (Deadline)
            else:
                for child in multiWorflow[each[0]][each[1]].outputs:
                    if  not([each[0],child.id] in tasklist): # tasklist
                        AST_child = multiWorflow[each[0]][child.id].StartTime
                        PreVMnum = multiWorflow[each[0]][child.id].VMnum
                        if [CloudID,VMnumID] == PreVMnum:
                            DataTransferRate = 0
                            TransTime = 0
                        else:
                            DataTransferRate = min(VMT[CloudID].B[VMS[CloudID][VMnumID].id],  VMT[PreVMnum[0]].B[VMS[PreVMnum[0]][PreVMnum[1]].id]   )
                            TransTime = (child.size/DataTransferRate * DTT)  #将传输时间放大DTT倍 
                        list_AST_TransT.append(AST_child-TransTime)
            if list_AST_TransT != []:        
                LFT.append(min(list_AST_TransT))
                AFT.append(multiWorflow[each[0]][each[1]].FinishTime)
        if LFT != []:         
            LFT_AFT = list(map(lambda x: x[0]-x[1], zip(LFT, AFT)))  #if LFT != []: 
            if len(tasklist)<len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID]):
                LFT_AFT.append( VMS[CloudID][VMnumID].VMTime[TaskCoreID][len(tasklist)][0]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][len(tasklist)-1][1] )
            if min(LFT_AFT)>0:                
                for i in range(len(tasklist)):
                    multiWorflow[tasklist[i][0]][tasklist[i][1]].FinishTime += min(LFT_AFT)
                    multiWorflow[tasklist[i][0]][tasklist[i][1]].StartTime  += min(LFT_AFT)
                    VMS[CloudID][VMnumID].VMTime[TaskCoreID][i][0] += min(LFT_AFT)
                    VMS[CloudID][VMnumID].VMTime[TaskCoreID][i][1] += min(LFT_AFT)  
                no_find_Block = False      

    while True:
        no_find_Block = True
        for CloudID in HYBRIDCLOUD:
            VMNums = len(VMS[CloudID])
            for VMnumID in range(VMNums):                                       #VM 
                for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores):                 #对应的核                
                    Totaltask = len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])
                    if Totaltask > 0:              #任务个数大于1
                        tasklist = [VMS[CloudID][VMnumID].TaskCore[TaskCoreID][0]]
                        for t_i in range(1,Totaltask):    #逐个任务
                            if VMS[CloudID][VMnumID].VMTime[TaskCoreID][t_i-1][1] == VMS[CloudID][VMnumID].VMTime[TaskCoreID][t_i][0]:
                                # 上一个任务的完成时间  == 当前任务的开始时间
                                tasklist.append(VMS[CloudID][VMnumID].TaskCore[TaskCoreID][t_i])#insert(len(tasklist),VMS[VMnumID].TaskCore[TaskCoreID][t_i])
                            else:
                                break     
                        AdjustListTasks()
        if no_find_Block: break

def Adjust_Scheduling():
    global VMS,multiWorflow  
    '''仅调整任务的开始和结束时间，结束时间设置为当前调度结果下的最晚结束时间''' 
    def AdjustListTasks():#tasklist,CloudID,VMnumID,TaskCoreID
        nonlocal no_find_Block
        # DelayTime = min{LFT,AFT} 延迟的时间
        # LFT :最晚完成时间，每个子任务的开始时间减去与该任务的传输时间  AFT：实际完成时间
        # TransTime:传输时间
        LFT = []
        AFT = []
        for each in tasklist:                            
            list_AST_TransT = []   #AST减去 传输时间
            if multiWorflow[each[0]][each[1]].outputs == []:
                list_AST_TransT.append(multiWorflow[each[0]][each[1]].FinishTime)   # AFT # (Deadline)
            else:
                for child in multiWorflow[each[0]][each[1]].outputs:
                    if  not([each[0],child.id] in tasklist): # tasklist
                        AST_child = multiWorflow[each[0]][child.id].StartTime
                        PreVMnum = multiWorflow[each[0]][child.id].VMnum
                        if [CloudID,VMnumID] == PreVMnum:
                            DataTransferRate = 0
                            TransTime = 0
                        else:
                            DataTransferRate = min(VMT[CloudID].B[VMS[CloudID][VMnumID].id],  VMT[PreVMnum[0]].B[VMS[PreVMnum[0]][PreVMnum[1]].id]   )
                            TransTime = (child.size/DataTransferRate * DTT)  #将传输时间放大DTT倍 
                        list_AST_TransT.append(AST_child-TransTime)
            if list_AST_TransT != []:        
                LFT.append(min(list_AST_TransT))
                AFT.append(multiWorflow[each[0]][each[1]].FinishTime)
        if LFT != []:         
            LFT_AFT = list(map(lambda x: x[0]-x[1], zip(LFT, AFT)))  #if LFT != []: 
            if tasklist[0]==VMS[CloudID][VMnumID].TaskCore[TaskCoreID][0]:
                if len(tasklist)<len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID]):
                    LFT_AFT.append( VMS[CloudID][VMnumID].VMTime[TaskCoreID][len(tasklist)][0]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][len(tasklist)-1][1] )
                if min(LFT_AFT)>0:                                
                    for i in range(len(tasklist)):
                        multiWorflow[tasklist[i][0]][tasklist[i][1]].FinishTime += min(LFT_AFT)
                        multiWorflow[tasklist[i][0]][tasklist[i][1]].StartTime  += min(LFT_AFT)
                        VMS[CloudID][VMnumID].VMTime[TaskCoreID][tasklist_index[i]][0] += min(LFT_AFT)
                        VMS[CloudID][VMnumID].VMTime[TaskCoreID][tasklist_index[i]][1] += min(LFT_AFT)
                    no_find_Block = False
            else:
                if len(tasklist)<len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID]):
                    LFT_AFT.append( VMS[CloudID][VMnumID].VMTime[TaskCoreID][Totaltask-1][0]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][Totaltask-2][1] )
                if min(LFT_AFT)>0:                  
                    # ll = Totaltask-2-len(tasklist)+1
                    # for i in range(Totaltask-2, Totaltask-2-len(tasklist),-1): 
                    for i in range(len(tasklist)):
                        multiWorflow[tasklist[i][0]][tasklist[i][1]].FinishTime += min(LFT_AFT)
                        multiWorflow[tasklist[i][0]][tasklist[i][1]].StartTime  += min(LFT_AFT)
                        VMS[CloudID][VMnumID].VMTime[TaskCoreID][tasklist_index[i]][0] += min(LFT_AFT)
                        VMS[CloudID][VMnumID].VMTime[TaskCoreID][tasklist_index[i]][1] += min(LFT_AFT)
                        # ll += 1  
                    no_find_Block = False

    while True:
        no_find_Block = True
        for CloudID in HYBRIDCLOUD:
            VMNums = len(VMS[CloudID])
            for VMnumID in range(VMNums):                                       #VM 
                for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores):                 #对应的核                
                    Totaltask = len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])
                    if Totaltask > 0:              #任务个数大于1
                        tasklist = [VMS[CloudID][VMnumID].TaskCore[TaskCoreID][0]]
                        tasklist_index = [0]
                        for t_i in range(1,Totaltask):    #逐个任务
                            if VMS[CloudID][VMnumID].VMTime[TaskCoreID][t_i-1][1] == VMS[CloudID][VMnumID].VMTime[TaskCoreID][t_i][0]:
                                # 上一个任务的完成时间  == 当前任务的开始时间
                                tasklist.append(VMS[CloudID][VMnumID].TaskCore[TaskCoreID][t_i])#insert(len(tasklist),VMS[VMnumID].TaskCore[TaskCoreID][t_i])
                                tasklist_index.append(t_i)
                            else:
                                break     
                        AdjustListTasks()
                    if (Totaltask > 2):
                        tasklist = [VMS[CloudID][VMnumID].TaskCore[TaskCoreID][Totaltask-2]]
                        tasklist_index = [Totaltask-2]
                        for t_i in range(Totaltask-2-1,0,-1):    #逐个任务
                            if VMS[CloudID][VMnumID].VMTime[TaskCoreID][t_i+1][0] == VMS[CloudID][VMnumID].VMTime[TaskCoreID][t_i][1]:
                                # 下一个任务的开始时间  == 当前任务的完成时间
                                tasklist.insert(0,VMS[CloudID][VMnumID].TaskCore[TaskCoreID][t_i])#insert(len(tasklist),VMS[VMnumID].TaskCore[TaskCoreID][t_i])
                                tasklist_index.insert(0,t_i)
                            else:
                                break     
                        AdjustListTasks()

        if no_find_Block: break

def getEST_MultiWorkflow(self,SimplifiedWorkflow,PCPfactor,PB_PCPfactor ,ddl):
    global HYBRIDCLOUD,PUBLICID,PRIVATEID,ListLevelVM
    NumPre = len(self.inputs)  #父节点的个数
    NumSuc = len(self.outputs) #子节点的个数  
    vmn = None                 #将要选择的VM
    taskcore = None            #将要选择的VM的核      
    EST = 0                 #最早开始时间
    listInputs = self.inputs

    CLOUD = [PRIVATEID] if self.MI==1 else HYBRIDCLOUD

    ################################################################################################
    '''以下内容采用活动化解码方式修改在每台VM上的可开始时间'''
    ## 父节点的完成时间
    listEST = [[] for j in range(2)]   
    for j in range(NumPre):
        listEST[0].append(listInputs[j].id)  
        listEST[1].append(SimplifiedWorkflow[listInputs[j].id].FinishTime)

    ### 以下采用混合云    
    EST_VM = [[],[]]  # 不考虑VM的完成时间时，任务在各VM上的可开始时间  
    for CloudID in CLOUD:
        VMNums = len(VMS[CloudID])
        for j1 in range(VMNums):
            EST_VM[CloudID].append([])
            for k in range(VMS[CloudID][j1].NumCores):
                EST_VM[CloudID][j1].append(0)
            for j in range(NumPre):
                PreVMnum = SimplifiedWorkflow[listEST[0][j]].VMnum
                if [CloudID,j1] == PreVMnum:
                    DataTransferRate = 0
                    DataTransferTime = 0
                else:                      
                    DataTransferRate = min(VMT[CloudID].B[VMS[CloudID][j1].id],  VMT[PreVMnum[0]].B[VMS[PreVMnum[0]][PreVMnum[1]].id]   )
                    DataTransferTime = (listInputs[j].size/DataTransferRate * DTT)  #将传输时间放大DTT倍 
                startTimePreDTT = listEST[1][j]+DataTransferTime
                for k in range(VMS[CloudID][j1].NumCores):
                    EST_VM[CloudID][j1][k] = max(EST_VM[CloudID][j1][k],startTimePreDTT) #,VMS[j1].CompleteTime[k]          
    ## 根据任务在每台VM的可开始时间 插空
    listESTVM = [[],[]] 
    ESTVMDifference = [[],[]] 
    for CloudID in CLOUD:
        VMNums = len(VMS[CloudID])    
        for j1 in range(VMNums):
            listESTVM[CloudID].append([])
            ESTVMDifference[CloudID].append([])
            for k in range(VMS[CloudID][j1].NumCores):
                listESTVM[CloudID][j1].append(EST_VM[CloudID][j1][k])
                ESTVMDifference[CloudID][j1].append(0)  
            find = False
            RT = self.runtime/VMT[CloudID].ProcessingCapacity[VMS[CloudID][j1].id]
            for k in range(VMS[CloudID][j1].NumCores):
                for h in range(len(VMS[CloudID][j1].VMTime[k])):
                    if EST_VM[CloudID][j1][k]<VMS[CloudID][j1].VMTime[k][h][0]:
                        t1 = 0 if h==0 else VMS[CloudID][j1].VMTime[k][h-1][1]
                        # if EST_VM[j1][k]>=t1:
                        if max(t1,EST_VM[CloudID][j1][k])+RT<=VMS[CloudID][j1].VMTime[k][h][0]:
                            listESTVM[CloudID][j1][k]=max(t1,EST_VM[CloudID][j1][k]) # +RT
                            ESTVMDifference[CloudID][j1][k]= listESTVM[CloudID][j1][k] - EST_VM[CloudID][j1][k]
                            find = True
                            break
                if find:
                    break
            if (not find):
                for k in range(VMS[CloudID][j1].NumCores):
                    listESTVM[CloudID][j1][k] = max(listESTVM[CloudID][j1][k],VMS[CloudID][j1].CompleteTime[k])
                    ESTVMDifference[CloudID][j1][k]= listESTVM[CloudID][j1][k] - VMS[CloudID][j1].CompleteTime[k]
    '''设置不超时的VM集合'''
    AvailableVM = [[],[]]
    for CloudID in CLOUD:
        VMNums = len(VMS[CloudID]) 
        for j in range(VMNums):
            if min(listESTVM[CloudID][j])+self.runtime/VMT[CloudID].ProcessingCapacity[VMS[CloudID][j].id]<self.XFT:
                AvailableVM[CloudID].append(j)

    ##  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # if ((((PCPfactor>=1)or(PCPfactor<0)) and((PB_PCPfactor>=1)or(PB_PCPfactor<0))) or(AvailableVM==[[],[]])):
    if (((not (0<=PCPfactor<1)) and(not(0<PB_PCPfactor<=1))) or(AvailableVM==[[],[]])):
        ### 错过deadline的 最早完成
        # listX =[]
        # for CloudID in CLOUD:
        #     for j in range(len(VMS[CloudID])):
        #         listX.append([CloudID,] )
        listX = [ [CloudID,j,min(listESTVM[CloudID][j])+self.runtime/VMT[CloudID].ProcessingCapacity[VMS[CloudID][j].id]] for CloudID in CLOUD for j in range(len(VMS[CloudID]))]
        indexlist = [listX[i][2] for i in range(len(listX))]
        vmn = [listX[indexlist.index(min(indexlist))][0], listX[indexlist.index(min(indexlist))][1]] #  

        EST = min(listESTVM[vmn[0]][vmn[1]])
        taskcore = listESTVM[vmn[0]][vmn[1]].index(EST) 
        return vmn,taskcore,EST
    # elif ((PB_PCPfactor>=0)and(PB_PCPfactor<1) and (((PCPfactor>=1)or(PCPfactor<0)) or(AvailableVM==[[],[]]) )):
    #     listX = []
    #     for j in range(len(AvailableVM[PUBLICID])):
    #         listX.append(min(listESTVM[PUBLICID][AvailableVM[PUBLICID][j]])+self.runtime/VMT[PUBLICID].ProcessingCapacity[VMS[PUBLICID][AvailableVM[PUBLICID][j]].id])
    #     # ### 某种规则  私有云增加0.5倍        
    #     listy = []
    #     for j in range(len(AvailableVM[PUBLICID])):  
    #         tempValue = (1+PUBLICID)*(ddl-listX[j])*self.runtime/VMT[PUBLICID].ProcessingCapacity[VMS[PUBLICID][AvailableVM[PUBLICID][j]].id]
    #         tempValue = tempValue/(min(ESTVMDifference[PUBLICID][AvailableVM[PUBLICID][j]])+1)
    #         listy.append(tempValue)          
    #     ###  取 最值及其索引
    #     maxVMIndex = listy.index(max(listy))
    #     vmn = [PUBLICID, AvailableVM[PUBLICID][maxVMIndex]]
    #     EST = min(listESTVM[vmn[0]][vmn[1]])
    #     taskcore = listESTVM[vmn[0]][vmn[1]].index(EST) 
    #     return vmn,taskcore,EST

    tempVMSet = [item for item in ListLevelVM if  item[1]  in AvailableVM[item[0]]] #
    if (taskcore == None)and(tempVMSet!=[]):  ## 上一层 VM 最早开始时间
        listX = [ round(min(listESTVM[j[0]][j[1]])*(1 - 0.9*j[0]),3) for j in tempVMSet]
        EST0 = min(listX)
        if listX.count(EST0)>1:
            Difference = []
            for i in range(len(tempVMSet)):# 
                if listX[i]==EST0:
                    Difference.append([tempVMSet[i],listX[i]-min(VMS[tempVMSet[i][0]][tempVMSet[i][1]].CompleteTime)])
            Dif = sorted(Difference, key=lambda Difference: Difference[1])
            vmn = Dif[0][0]  
            for i1 in range(1,len(Dif)):
                if (Dif[i1][1] == Dif[0][1]) and (VMS[vmn[0]][vmn[1]].id<VMS[Dif[i1][0][0]][Dif[i1][0][1]] .id):# 3):# and(vmn<Dif[0][0]+3): # GlobalResource.SuitVM):#
                    vmn = Dif[i1][0]
                    break
        else:
            vmn = tempVMSet[listX.index(EST0)]              
        EST = min(listESTVM[vmn[0]][vmn[1]])
        if (EST+self.runtime/VMT[vmn[0]].ProcessingCapacity[VMS[vmn[0]][vmn[1]].id]<=min(self.XFT,LevelMaxFinishTtime)): #self.XFT):  #
            taskcore = listESTVM[vmn[0]][vmn[1]].index(EST)
            return vmn,taskcore,EST

        # else:
    if taskcore == None: 
        #####  在可用VM中选择
        # listX1 = [ [CloudID,min(listESTVM[CloudID][AvailableVM[CloudID][j]])+self.runtime/VMT[CloudID].ProcessingCapacity[VMS[CloudID][AvailableVM[CloudID][j]].id]] for CloudID in CLOUD for j in range(len(AvailableVM[CloudID]))]
        listX = [[],[]]
        for CloudID in CLOUD:
            for j in range(len(AvailableVM[CloudID])):
                listX[CloudID].append(min(listESTVM[CloudID][AvailableVM[CloudID][j]])+self.runtime/VMT[CloudID].ProcessingCapacity[VMS[CloudID][AvailableVM[CloudID][j]].id])
        ### 最早完成
        # vmn = listX.index(min(listX)) 
        # ### 某种规则  私有云增加0.5倍        
        # listy = [(1+0.5*CloudID)*(ddl-listX[CloudID][j])*self.runtime/VMT[CloudID].ProcessingCapacity[VMS[CloudID][AvailableVM[CloudID][j]].id] for CloudID in CLOUD for j in range(len(AvailableVM[CloudID]))]
        listy = [[],[]]
        for CloudID in CLOUD:
            for j in range(len(AvailableVM[CloudID])):  
                tempValue = (1+CloudID)*(ddl-listX[CloudID][j])*self.runtime/VMT[CloudID].ProcessingCapacity[VMS[CloudID][AvailableVM[CloudID][j]].id]
                tempValue = tempValue/(min(ESTVMDifference[CloudID][AvailableVM[CloudID][j]])+1)
                listy[CloudID].append(tempValue)          
        ###  取 最值及其索引
        # maxList = [max(listy[CloudID]) for CloudID in CLOUD]
        maxList = []
        for CloudID in CLOUD:
            if listy[CloudID]==[]:
                maxList.append(-inf)
            else:
                maxList.append(max(listy[CloudID]))
        maxIDIndex = CLOUD[maxList.index(max(maxList))] # maxIDIndex
        maxVMIndex = listy[maxIDIndex].index(max(listy[maxIDIndex]))
        vmn = [maxIDIndex, AvailableVM[maxIDIndex][maxVMIndex]]
        EST = min(listESTVM[vmn[0]][vmn[1]])
        taskcore = listESTVM[vmn[0]][vmn[1]].index(EST) 
        return vmn,taskcore,EST

def CalcaulateTaskObject_MultiWorkflow(workflowNum,taskID,vmn,taskcore,EST):
    multiWorflow[workflowNum][taskID].VMnum = vmn
    multiWorflow[workflowNum][taskID].VMcore = taskcore 
    multiWorflow[workflowNum][taskID].StartTime = EST           # min(VMS[vmn].CompleteTime)
    multiWorflow[workflowNum][taskID].FinishTime = EST + (multiWorflow[workflowNum][taskID].runtime/VMT[vmn[0]].ProcessingCapacity[VMS[vmn[0]][vmn[1]].id])
    if EST>=VMS[vmn[0]][vmn[1]].CompleteTime[taskcore]:
        VMS[vmn[0]][vmn[1]].CompleteTime[taskcore] = multiWorflow[workflowNum][taskID].FinishTime
        VMS[vmn[0]][vmn[1]].TaskCore[taskcore].insert(len(VMS[vmn[0]][vmn[1]].TaskCore[taskcore]),[workflowNum,taskID])        
        list1 = list([multiWorflow[workflowNum][taskID].StartTime,multiWorflow[workflowNum][taskID].FinishTime])
        VMS[vmn[0]][vmn[1]].VMTime[taskcore].insert(len(VMS[vmn[0]][vmn[1]].VMTime[taskcore]),list1)
    else:
        for h in range(len(VMS[vmn[0]][vmn[1]].VMTime[taskcore])):
            if multiWorflow[workflowNum][taskID].FinishTime<VMS[vmn[0]][vmn[1]].VMTime[taskcore][h][0]:
                VMS[vmn[0]][vmn[1]].TaskCore[taskcore].insert(h,[workflowNum,taskID])                    
                list1 = list([multiWorflow[workflowNum][taskID].StartTime,multiWorflow[workflowNum][taskID].FinishTime])
                VMS[vmn[0]][vmn[1]].VMTime[taskcore].insert(h,list1)
                break     

def Urgency(multiWorflowLevel,multiDeadline,FT_Star,ScheduledMultiWFLevel):  
    global HYBRIDCLOUD #PRIVATEID 
    multiWorflowPCP = [[],[]]
    multiUrgency  = [[],[]]
    for CloudID in HYBRIDCLOUD:
        for i in range(len(multiWorflowLevel)): # 工作流
            listExcuteTime = []
            for j in range(ScheduledMultiWFLevel[i], len(multiWorflowLevel[i])): # 工作流的层 multiWorflowLevel[i][j][k] 对应任务 
                # 下面4句简写
                tempTime = 0           
                for k in range(len(multiWorflowLevel[i][j])):
                    taskID = multiWorflowLevel[i][j][k]
                    if multiWorflow[i][taskID].runtime/max(VMT[CloudID].ProcessingCapacity)>tempTime:
                        tempTime = multiWorflow[i][taskID].runtime/max(VMT[CloudID].ProcessingCapacity)  ## 在配置最高的VM
                listExcuteTime.append(tempTime)
            if listExcuteTime != []:
                multiUrgency[CloudID].append([i,sum(listExcuteTime)/(multiDeadline[i]['Deadline']-FT_Star[i])])
                multiWorflowPCP[CloudID].append([i,sum(listExcuteTime)])
            else:
                multiUrgency[CloudID].append([i,float('-inf')])
                multiWorflowPCP[CloudID].append([i,float('-inf')])

    return multiUrgency,multiWorflowPCP
        
def HeuristicIndividual():
    global PUBLICID,PRIVATEID,multiWorflow,VMS,multiWorflowDAGLevel,LevelMaxFinishTtime,FT_Star,ListLevelVM,OriginalMWOrder
    DiscrSalp = []
    multiWorflowDAGLevel = copy.deepcopy(tempmultiWorflowDAGLevel)
    multiWorflow = copy.deepcopy(tempmultiWorflow)
    VMS = copy.deepcopy(tempVMS)    

    VM_AssignedTask = [] #set()
    UsedPRIVATE = [0 for i in PrivateCloudVMType().P]

    LevelMaxFinishTtime = 0 # 当前的最大完工时间
    
    FT_Star=[0 for i in range(len(multiWorflow))] # 每个工作流的当前最大完成时间
    TotalLevel = sum([len(multiWorflowDAGLevel[i]) for i in range(len(multiWorflowDAGLevel))])
    ScheduledMultiWFLevel = [0 for i in range(len(multiWorflow))] # 每个工作流已调度的层数
    for kk in range(TotalLevel):
        multiUrgency,multiWorflowPCP = Urgency(multiWorflowDAGLevel,multiWorflowDeadline,FT_Star,ScheduledMultiWFLevel)
        templist = [multiUrgency[PRIVATEID][i][1] for i in range(len(multiUrgency[PRIVATEID]))]    # multiUrgency[PRIVATEID][:][1]        
        maxIndex = templist.index(max(templist))
        workflowNum = multiUrgency[PRIVATEID][maxIndex][0]# 基于上述规则
        DiscrSalp.append(workflowNum)
        ListLevelVM = [] ###  上层任务所部属的VM
        for i in range(len(multiWorflow)):
            levelNum = ScheduledMultiWFLevel[i]-1
            if levelNum>0:            
                for taskid in tempmultiWorflowDAGLevel[i][levelNum-1]:
                    if multiWorflow[i][taskid].VMnum not in ListLevelVM:
                        ListLevelVM.append(multiWorflow[i][taskid].VMnum)                 
                for taskid in tempmultiWorflowDAGLevel[i][levelNum]:                   
                    for parent in multiWorflow[i][taskid].inputs:
                        if multiWorflow[i][parent.id].VMnum not in ListLevelVM:
                            ListLevelVM.append(multiWorflow[i][parent.id].VMnum)
            elif levelNum==0:
                for taskid in tempmultiWorflowDAGLevel[i][levelNum]:                   
                    for parent in multiWorflow[i][taskid].inputs:
                        if multiWorflow[i][parent.id].VMnum not in ListLevelVM:
                            ListLevelVM.append(multiWorflow[i][parent.id].VMnum)                
        
        for taskID in multiWorflowDAGLevel[workflowNum][ScheduledMultiWFLevel[workflowNum]] :      # tilde_Pai[workflowNum][workflowNum]:
            vmn,taskcore,EST = getEST_MultiWorkflow(multiWorflow[workflowNum][taskID],multiWorflow[workflowNum],
                            multiUrgency[PRIVATEID][maxIndex][1],multiUrgency[PUBLICID][maxIndex][1],multiWorflowDeadline[workflowNum]['Deadline']) # getEST(multiWorflow[workflowNum][taskID])
            CalcaulateTaskObject_MultiWorkflow(workflowNum,taskID,vmn,taskcore,EST)
            FT_Star[workflowNum] = max(FT_Star[workflowNum],multiWorflow[workflowNum][taskID].FinishTime)
            LevelMaxFinishTtime = max(LevelMaxFinishTtime,multiWorflow[workflowNum][taskID].FinishTime)
            if not (vmn in VM_AssignedTask):
                VM_AssignedTask.append(vmn)
                ## 此处需要判断是否满足 VM 数量限制
                if vmn[0]==PRIVATEID: # 私有
                    UsedPRIVATE[VMS[vmn[0]][vmn[1]].id] += 1
                    if UsedPRIVATE[VMS[vmn[0]][vmn[1]].id]<GlobalResource.NUMofPrivateCloudVM[VMS[vmn[0]][vmn[1]].id]:
                        VMS[vmn[0]].append(VMScheduling(VMT[vmn[0]].P[VMS[vmn[0]][vmn[1]].id], VMT[vmn[0]].N[VMS[vmn[0]][vmn[1]].id]))
                else:
                    VMS[vmn[0]].append(VMScheduling(VMT[vmn[0]].P[VMS[vmn[0]][vmn[1]].id], VMT[vmn[0]].N[VMS[vmn[0]][vmn[1]].id]))
            if vmn not in ListLevelVM:
                ListLevelVM.append(vmn)      
        ScheduledMultiWFLevel[workflowNum] += 1  

    Adjust_Scheduling()
    # Adaptively_Adjust_First_Task_Block_Multiworkflow()

    Obj = GlobalResource.caculateMultiWorkflowMakespan_Cost(multiWorflow,WfDeadline,VMS)
    HeuriSalp = SalpClass()
    HeuriSalp.DiscrSalp = DiscrSalp
    HeuriSalp.multiworflow =multiWorflow
    HeuriSalp.VMSchedule = VMS
    HeuriSalp.objectives = Obj
    HeuriSalp.LevelTask = multiWorflowDAGLevel
    # OriginalMWOrder = [i for i in range(len(ScheduledMultiWFLevel)) for j in range(ScheduledMultiWFLevel[i])]
    HeuriSalp.ContiSalp = Discrete_to_Continuous_SOV_rule(HeuriSalp.DiscrSalp) # ,OriginalMWOrder
    return HeuriSalp # DiscrSalp,multiWorflow,VMS,Obj



def MateHeuristicIndividual_noLevelTask(Salp):
    global PUBLICID,PRIVATEID,multiWorflow,VMS,multiWorflowDAGLevel,LevelMaxFinishTtime,FT_Star,ListLevelVM
    # DiscreteLevel_order 
    multiWorflowDAGLevel = copy.deepcopy(tempmultiWorflowDAGLevel)
    multiWorflow = copy.deepcopy(tempmultiWorflow)
    VMS = copy.deepcopy(tempVMS)    
    
    # vmn = [PRIVATEID,VMT[PRIVATEID].ProcessingCapacity.index(max(VMT[PRIVATEID].ProcessingCapacity)) ]
    VM_AssignedTask = [] #set()
    UsedPRIVATE = [0 for i in PrivateCloudVMType().P]

    LevelMaxFinishTtime = 0 # 当前的最大完工时间

    FT_Star=[0 for i in range(len(multiWorflow))] # 每个工作流的当前最大完成时间
    TotalLevel = sum([len(multiWorflowDAGLevel[i]) for i in range(len(multiWorflowDAGLevel))])
    ScheduledMultiWFLevel = [0 for i in range(len(multiWorflow))] # 每个工作流已调度的层数    
    for workflowNum in Salp.DiscrSalp: #DiscreteLevel_order
        multiUrgency,multiWorflowPCP = Urgency(multiWorflowDAGLevel,multiWorflowDeadline,FT_Star,ScheduledMultiWFLevel)
        ListLevelVM = [] ###  上层任务所部属的VM
        for i in range(len(multiWorflow)):
            levelNum = ScheduledMultiWFLevel[i]-1 #len(tempmultiWorflowDAGLevel[i])-len(multiWorflowDAGLevel[i])-1   #  max(len(multiWorflowDAGLevel[i]),1)#-1
            if levelNum>0:
                for taskid in tempmultiWorflowDAGLevel[i][levelNum-1]:
                    if multiWorflow[i][taskid].VMnum not in ListLevelVM:
                        ListLevelVM.append(multiWorflow[i][taskid].VMnum)                 
                for taskid in tempmultiWorflowDAGLevel[i][levelNum]:                   
                    for parent in multiWorflow[i][taskid].inputs:
                        if multiWorflow[i][parent.id].VMnum not in ListLevelVM:
                            ListLevelVM.append(multiWorflow[i][parent.id].VMnum)
            elif levelNum==0:
                for taskid in tempmultiWorflowDAGLevel[i][levelNum]:                   
                    for parent in multiWorflow[i][taskid].inputs:
                        if multiWorflow[i][parent.id].VMnum not in ListLevelVM:
                            ListLevelVM.append(multiWorflow[i][parent.id].VMnum)                            
        random.shuffle(multiWorflowDAGLevel[workflowNum][ScheduledMultiWFLevel[workflowNum]]) # 随机顺序
        for taskID in multiWorflowDAGLevel[workflowNum][ScheduledMultiWFLevel[workflowNum]]:
            vmn,taskcore,EST = getEST_MultiWorkflow(multiWorflow[workflowNum][taskID],multiWorflow[workflowNum],
                            multiUrgency[PRIVATEID][workflowNum][1],multiUrgency[PUBLICID][workflowNum][1],multiWorflowDeadline[workflowNum]['Deadline']) # getEST(multiWorflow[workflowNum][taskID])
            CalcaulateTaskObject_MultiWorkflow(workflowNum,taskID,vmn,taskcore,EST)
            FT_Star[workflowNum] = max(FT_Star[workflowNum],multiWorflow[workflowNum][taskID].FinishTime)
            LevelMaxFinishTtime = max(LevelMaxFinishTtime,multiWorflow[workflowNum][taskID].FinishTime)
            if not (vmn in VM_AssignedTask):
                VM_AssignedTask.append(vmn)
                ## 此处需要判断是否满足 VM 数量限制
                if vmn[0]==PRIVATEID: # 私有
                    UsedPRIVATE[VMS[vmn[0]][vmn[1]].id] += 1
                    if UsedPRIVATE[VMS[vmn[0]][vmn[1]].id]<GlobalResource.NUMofPrivateCloudVM[VMS[vmn[0]][vmn[1]].id]:
                        VMS[vmn[0]].append(VMScheduling(VMT[vmn[0]].P[VMS[vmn[0]][vmn[1]].id], VMT[vmn[0]].N[VMS[vmn[0]][vmn[1]].id]))
                else:
                    VMS[vmn[0]].append(VMScheduling(VMT[vmn[0]].P[VMS[vmn[0]][vmn[1]].id], VMT[vmn[0]].N[VMS[vmn[0]][vmn[1]].id]))
            if vmn not in ListLevelVM:
                ListLevelVM.append(vmn)           
        ScheduledMultiWFLevel[workflowNum] += 1
        # if multiWorflowDAGLevel[workflowNum]!=[]:
        #     tilde_Pai[workflowNum].update({workflowNum:multiWorflowDAGLevel[workflowNum][0]})
        # else:
        #     tilde_Pai[workflowNum].update({workflowNum:[]})
        # # if sum([len(multiWorflowDAGLevel[i]) for i in range(len(multiWorflowDAGLevel))])==0:
        # #     break
    Adjust_Scheduling()
    # Adaptively_Adjust_First_Task_Block_Multiworkflow()

    Obj = GlobalResource.caculateMultiWorkflowMakespan_Cost(multiWorflow,WfDeadline,VMS)
    Salp.multiworflow =multiWorflow
    Salp.VMSchedule = VMS
    Salp.objectives = Obj
    Salp.LevelTask = multiWorflowDAGLevel
    return Salp # multiWorflow,VMS,Obj

def MateHeuristicIndividual(Salp):
    global PUBLICID,PRIVATEID,multiWorflow,VMS,multiWorflowDAGLevel,LevelMaxFinishTtime,FT_Star,ListLevelVM  # 
    # DiscreteLevel_order 
    # multiWorflowDAGLevel = copy.deepcopy(tempmultiWorflowDAGLevel)
    multiWorflow = copy.deepcopy(tempmultiWorflow)
    VMS = copy.deepcopy(tempVMS)   
    
    
    # vmn = [PRIVATEID,VMT[PRIVATEID].ProcessingCapacity.index(max(VMT[PRIVATEID].ProcessingCapacity)) ]
    VM_AssignedTask = [] #set()
    UsedPRIVATE = [0 for i in PrivateCloudVMType().P]

    LevelMaxFinishTtime = 0 # 当前的最大完工时间

    FT_Star=[0 for i in range(len(multiWorflow))] # 每个工作流的当前最大完成时间
    TotalLevel = sum([len(Salp.LevelTask[i]) for i in range(len(Salp.LevelTask))])
    ScheduledMultiWFLevel = [0 for i in range(len(multiWorflow))] # 每个工作流已调度的层数    
    for workflowNum in Salp.DiscrSalp: #DiscreteLevel_order
        multiUrgency,multiWorflowPCP = Urgency(Salp.LevelTask,multiWorflowDeadline,FT_Star,ScheduledMultiWFLevel)
        ListLevelVM = [] ###  上层任务所部属的VM
        for i in range(len(multiWorflow)):
            levelNum = ScheduledMultiWFLevel[i]-1 #len(tempmultiWorflowDAGLevel[i])-len(multiWorflowDAGLevel[i])-1   #  max(len(multiWorflowDAGLevel[i]),1)#-1
            if levelNum>0:
                for taskid in tempmultiWorflowDAGLevel[i][levelNum-1]:
                    if multiWorflow[i][taskid].VMnum not in ListLevelVM:
                        ListLevelVM.append(multiWorflow[i][taskid].VMnum)                 
                for taskid in tempmultiWorflowDAGLevel[i][levelNum]:                   
                    for parent in multiWorflow[i][taskid].inputs:
                        if multiWorflow[i][parent.id].VMnum not in ListLevelVM:
                            ListLevelVM.append(multiWorflow[i][parent.id].VMnum)
        # random.shuffle(multiWorflowDAGLevel[workflowNum][ScheduledMultiWFLevel[workflowNum]]) # 随机顺序
        for taskID in Salp.LevelTask[workflowNum][ScheduledMultiWFLevel[workflowNum]]:
            vmn,taskcore,EST = getEST_MultiWorkflow(multiWorflow[workflowNum][taskID],multiWorflow[workflowNum],
                            multiUrgency[PRIVATEID][workflowNum][1],multiUrgency[PUBLICID][workflowNum][1],multiWorflowDeadline[workflowNum]['Deadline']) # getEST(multiWorflow[workflowNum][taskID])
            CalcaulateTaskObject_MultiWorkflow(workflowNum,taskID,vmn,taskcore,EST)
            FT_Star[workflowNum] = max(FT_Star[workflowNum],multiWorflow[workflowNum][taskID].FinishTime)
            LevelMaxFinishTtime = max(LevelMaxFinishTtime,multiWorflow[workflowNum][taskID].FinishTime)
            if not (vmn in VM_AssignedTask):
                VM_AssignedTask.append(vmn)
                ## 此处需要判断是否满足 VM 数量限制
                if vmn[0]==PRIVATEID: # 私有
                    UsedPRIVATE[VMS[vmn[0]][vmn[1]].id] += 1
                    if UsedPRIVATE[VMS[vmn[0]][vmn[1]].id]<GlobalResource.NUMofPrivateCloudVM[VMS[vmn[0]][vmn[1]].id]:
                        VMS[vmn[0]].append(VMScheduling(VMT[vmn[0]].P[VMS[vmn[0]][vmn[1]].id], VMT[vmn[0]].N[VMS[vmn[0]][vmn[1]].id]))
                else:
                    VMS[vmn[0]].append(VMScheduling(VMT[vmn[0]].P[VMS[vmn[0]][vmn[1]].id], VMT[vmn[0]].N[VMS[vmn[0]][vmn[1]].id]))
            if vmn not in ListLevelVM:
                ListLevelVM.append(vmn)           
        ScheduledMultiWFLevel[workflowNum] += 1
        # if multiWorflowDAGLevel[workflowNum]!=[]:
        #     tilde_Pai[workflowNum].update({workflowNum:multiWorflowDAGLevel[workflowNum][0]})
        # else:
        #     tilde_Pai[workflowNum].update({workflowNum:[]})
        # # if sum([len(multiWorflowDAGLevel[i]) for i in range(len(multiWorflowDAGLevel))])==0:
        # #     break
    Adjust_Scheduling()
    # Adaptively_Adjust_First_Task_Block_Multiworkflow()

    Obj = GlobalResource.caculateMultiWorkflowMakespan_Cost(multiWorflow,WfDeadline,VMS)
    Salp.multiworflow =multiWorflow
    Salp.VMSchedule = VMS
    Salp.objectives = Obj
    # Salp.LevelTask = multiWorflowDAGLevel
    return Salp # multiWorflow,VMS,Obj


class solution:
    def __init__(self):
        self.best = 0
        self.bestIndividual=[]
        self.convergence = []
        self.optimizer=""
        self.objfname=""
        self.startTime=0
        self.endTime=0
        self.executionTime=0
        self.lb=0
        self.ub=0
        self.dim=0
        self.popnum=0
        self.maxiers=0

def Continuous_to_Discrete_SOV_rule(Continuous_order): # ,Level
    global OriginalMWOrder
    # Discrete_order = []
    x = Continuous_order[:]
    temp_x = Continuous_order[:]
    x.sort()
    y = []
    for i in range(len(x)):
        y.append(x.index(temp_x[i]))
        x[x.index(temp_x[i])] = -inf
    Discrete_order = [OriginalMWOrder[i] for i in y]
    return Discrete_order

def Discrete_to_Continuous_SOV_rule(Discrete_order): # ,Level
    global OriginalMWOrder
    # Continuous_order = []
    x = [random.uniform(-10,10) for i in range(len(OriginalMWOrder))] # Discrete_order[:]  # random.randint(0,3)
    x.sort() # np.sort(x)
    # temp_x = Discrete_order[:]
    temp_L = OriginalMWOrder[:]
    Continuous_order = [0 for i in range(len(x))]

    for i in range(len(x)):
        dex = temp_L.index(Discrete_order[i])
        temp_L[dex]= -inf
        Continuous_order[i] = x[dex]  
        
    # y = Continuous_to_Discrete_SOV_rule(Continuous_order,Level)
    return Continuous_order    
####################################################################################################################

class SalpClass:
    def __init__(self):
        self.ContiSalp=None
        self.DiscrSalp=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.LevelTask=None

def InitializeSalpPopulation(popsize):
    global OriginalMWOrder
    SalpPopulation = []
    for g in range(popsize):
        SalpPopulation.append(SalpClass())
        SalpPopulation[g].ContiSalp = [random.uniform(-10,10) for i in range(len(OriginalMWOrder))]  # random.randint(0,3)
        SalpPopulation[g].DiscrSalp = Continuous_to_Discrete_SOV_rule(SalpPopulation[g].ContiSalp) # ,OriginalMWOrder
        # SalpPopulation[g].multiworflow,SalpPopulation[g].VMSchedule,SalpPopulation[g].objectives = MateHeuristicIndividual(SalpPopulation[g].DiscrSalp)
        SalpPopulation[g].LevelTask = copy.deepcopy(tempmultiWorflowDAGLevel)
        for i in range(len(SalpPopulation[g].LevelTask)):
            for j in range(len(SalpPopulation[g].LevelTask[i])):
                random.shuffle(SalpPopulation[g].LevelTask[i][j]) # 随机顺序
        SalpPopulation[g] = MateHeuristicIndividual(SalpPopulation[g])
        # gantt_VMState_MultiWorkflow(SalpPopulation[g].VMSchedule,SalpPopulation[g].multiworflow,SalpPopulation[g].objectives)
    return SalpPopulation


def non_dominatedSalps(SalpPopulation,NumNonDominated):
    NonDominSalps = []
    for i in range(len(SalpPopulation)):
        b_non_dominated = True
        for j in range(len(SalpPopulation)):
            if (j!=i) and GlobalResource.DetermineWhether2Dominate(SalpPopulation[j],SalpPopulation[i]):
                b_non_dominated = False
                break
        if b_non_dominated:
            NonDominSalps.append(SalpPopulation[i])
    

    NonDominSalps.sort(key=operator.attrgetter('objectives.Energy','objectives.Cost'))
    if len(NonDominSalps)>1:
        kk= 0
        while True:
            i = kk +1 
            # if ((NonDominSalps[i].objectives.Cost==NonDominSalps[kk].objectives.Cost) and(NonDominSalps[i].objectives.Energy==NonDominSalps[kk].objectives.Energy)):
            if GlobalResource.DetermineWhether2Equal(NonDominSalps[i],NonDominSalps[kk]):
                NonDominSalps.pop(i)
            else:
                kk += 1
            if kk>=len(NonDominSalps)-1:
                break
        
    return NonDominSalps

def CalcuCrowdDistance_UpdateNon_domin(Salps,NumNonDominated):
    if NumNonDominated<len(Salps):
        listCost = [salp.objectives.Cost for salp in Salps]
        listEnergy = [salp.objectives.Energy for salp in Salps]
        listTardiness = [salp.objectives.TotalTardiness for salp in Salps]
        maxCost,minCost = max(listCost),min(listCost)
        maxEnergy,minEnergy = max(listEnergy),min(listEnergy)
        maxTardiness,minTardiness = max(listTardiness),min(listTardiness)
        CrowdingDistance = []
        minmaxIndex = [0,  len(Salps)-1]
        for i in range(len(Salps)):
            if i in minmaxIndex:
                CrowdingDistance.append([i,inf])
            else:
                CrowdingDistance.append([i,0])
                if (maxCost!=minCost):            
                    CrowdingDistance[i][1] += abs(Salps[i-1].objectives.Cost-Salps[i+1].objectives.Cost)/(maxCost-minCost)
                if (maxEnergy!=minEnergy):            
                    CrowdingDistance[i][1] += abs(Salps[i-1].objectives.Energy-Salps[i+1].objectives.Energy)/(maxEnergy-minEnergy)    
                if (maxTardiness!=minTardiness):            
                    CrowdingDistance[i][1] += abs(Salps[i-1].objectives.TotalTardiness-Salps[i+1].objectives.TotalTardiness)/(maxTardiness-minTardiness)        
        CrowdingDistance = sorted(CrowdingDistance, key=lambda CrowdingDistance: CrowdingDistance[1])   # ,reverse=True
        # tempSalpPopulation = SalpPopulation[:]
        NonSalps = []
        templist = [CrowdingDistance[i][0] for i in range(len(Salps)-NumNonDominated) ]
        for i in range(len(Salps)): # len(Salps)-NumNonDominated,
            if i not in templist:
                NonSalps.append(Salps[i])     # i    
        return NonSalps
    else:
        return Salps

### 以下同原程序
## 非支配解的与上面的相同
def RankingProcess(Salps):
    # if NumNonDominated<len(Salps):
    listCost = [salp.objectives.Cost for salp in Salps]
    listEnergy = [salp.objectives.Energy for salp in Salps]
    maxCost,minCost = max(listCost),min(listCost)
    maxEnergy,minEnergy = max(listEnergy),min(listEnergy)
    listTardiness = [salp.objectives.TotalTardiness for salp in Salps]
    maxTardiness,minTardiness = max(listTardiness),min(listTardiness)
    radius = [(maxCost-minCost)/20,(maxEnergy-minEnergy)/20,(maxTardiness-minTardiness)/20 ] # 半径
    ranks = []
    for i in range(len(Salps)):
        ranks.append(1)
        for j in range(len(Salps)):
            flag = 0
            if abs(Salps[i].objectives.Cost-Salps[j].objectives.Cost)<radius[0]:
                flag += 1
            if abs(Salps[i].objectives.Energy-Salps[j].objectives.Energy)<radius[1]:
                flag += 1   
            if abs(Salps[i].objectives.TotalTardiness-Salps[j].objectives.TotalTardiness)<radius[2]:
                flag += 1                  
            if flag == 3:
                ranks[i] +=1
    return ranks

def RouletteWheelSelection(weights):
    accumulation = sum(weights)
    p = random.random()
    chosen_index = 0
    for index in range(len(weights)):
        chosen_index += weights[index]/accumulation 
        if (chosen_index > p):
            choice = index
            break 
    return choice

def HandleFullArchive(Salps,ranks, NumNonDominated):
    k = len(Salps)-NumNonDominated
    for i in range(k):
        index = RouletteWheelSelection(ranks)
        Salps.pop(index)
        ranks.pop(index)
    return Salps

def LocalSearch_Salp(oldSalp):
    global OriginalMWOrder
    ''' Destruction and reconstruction 破坏与重构
        Destruction: 随机 从序列中选取 【序列长度/工作流个数，2*序列长度/工作流个数】
    '''
    Salp = copy.deepcopy(oldSalp)
    for kkkk in range(10):
        # Salp = copy.deepcopy(oldSalp)
        ###   level 的序列  
        numbers = random.randint(math.trunc(len(OriginalMWOrder)/len(Salp.multiworflow) ), math.trunc(2*len(OriginalMWOrder)/len(Salp.multiworflow)))
        poplist = [ Salp.DiscrSalp.pop(random.randint(0,len(Salp.DiscrSalp)-1)) for i in range(numbers) ]
        for each in poplist:
            Salp.DiscrSalp.insert(random.randint(0,len(Salp.DiscrSalp)),each)

        ###   每层task的序列 [1,2]
        for i in range(len(Salp.LevelTask)):
            for j in range(len(Salp.LevelTask[i])):
                if len(Salp.LevelTask[i][j])>2:
                    numbers = random.randint(1,math.trunc(len(Salp.LevelTask[i][j])/2))
                    k =1
                    poplist = [ Salp.LevelTask[i][j].pop(random.randint(0,len(Salp.LevelTask[i][j])-1)) for i1 in range(numbers) ]
                    for each in poplist:
                        Salp.LevelTask[i][j].insert(random.randint(0,len(Salp.LevelTask[i][j])),each)
                elif len(Salp.LevelTask[i][j])==2:
                    if random.random()<0.5:
                        k =1 
                        Salp.LevelTask[i][j][0],Salp.LevelTask[i][j][1] = Salp.LevelTask[i][j][1],Salp.LevelTask[i][j][0]
                        
        Salp = MateHeuristicIndividual(Salp)
        if GlobalResource.DetermineWhether2Dominate(Salp,oldSalp):
            Salp.ContiSalp = Discrete_to_Continuous_SOV_rule(Salp.DiscrSalp)
            # oldSalp = Salp
            # Salp = copy.deepcopy(oldSalp)
            return Salp
        # Salp.DiscrSalp = oldSalp.DiscrSalp
    return oldSalp
 
def MSSA(): 
    global  OriginalMWOrder  
    popsize = 30
    NumNonDominated = 20
    max_iter = 100
    UP = 10
    DOWN = -10 # DOWN,UP
    GAP = UP-DOWN
    AlgorithmStart = time.time()
    SalpPopulation = InitializeSalpPopulation(popsize-1) #,OriginalMWOrder
    SalpPopulation.append(SalpClass())
    SalpPopulation[popsize-1] = HeuristicIndividual()
    # SalpPopulation[popsize-1].DiscrSalp,SalpPopulation[popsize-1].multiworflow,SalpPopulation[popsize-1].VMSchedule,SalpPopulation[popsize-1].objectives = HeuristicIndividual() # 
    # SalpPopulation[popsize-1].ContiSalp = Discrete_to_Continuous_SOV_rule(SalpPopulation[popsize-1].DiscrSalp,OriginalMWOrder)
    NonDominSalps = [] # non_dominatedSalps(SalpPopulation,NumNonDominated) 
    for iter in range(max_iter):
        c1 = 2*math.exp(pow(-(4*iter/max_iter),2))
        NonDominSalps = copy.deepcopy(NonDominSalps) + copy.deepcopy(SalpPopulation)
        NonDominSalps = non_dominatedSalps(NonDominSalps,NumNonDominated)

        # np.save(os.getcwd()+'/ParetoFront/'+'1.npy', NonDominSalps)
        # # np.save(os.getcwd()+'/ResultExcel/'+'2.npy', NonDominSalps)
        # kk = np.load(os.getcwd()+'/ParetoFront/'+'1.npy',allow_pickle=True)


        if len(NonDominSalps)>NumNonDominated:
            ranks = RankingProcess(NonDominSalps)
            NonDominSalps = HandleFullArchive(NonDominSalps,ranks, NumNonDominated)
        # else:
        #     ranks = RankingProcess(NonDominSalps)
        if len(NonDominSalps)>1:
            ranks = RankingProcess(NonDominSalps)
            ranks = [1/i for i in ranks]
            FoodIndex = RouletteWheelSelection(ranks)
            Food = NonDominSalps[FoodIndex]
        else:
            Food = NonDominSalps[0]

        for i in range(popsize):
            if i<=popsize/2:
                for j in range(len(OriginalMWOrder)):
                    c2 = random.random()
                    c3 = random.random()
                    if c3<0.5:
                        SalpPopulation[i].ContiSalp[j] = Food.ContiSalp[j] +c1*random.uniform(DOWN,UP)
                    else:
                        SalpPopulation[i].ContiSalp[j] = Food.ContiSalp[j] -c1*random.uniform(DOWN,UP)
            else:
                for j in range(len(OriginalMWOrder)):
                    SalpPopulation[i].ContiSalp[j] = (SalpPopulation[i].ContiSalp[j] +SalpPopulation[i-1].ContiSalp[j])/2
            SalpPopulation[i].ContiSalp = [(GAP*(SalpPopulation[i].ContiSalp[j] -min(SalpPopulation[i].ContiSalp))/
                                               (max(SalpPopulation[i].ContiSalp)-min(SalpPopulation[i].ContiSalp))) 
                                            for j in range(len(OriginalMWOrder))]
            SalpPopulation[i].DiscrSalp = Continuous_to_Discrete_SOV_rule(SalpPopulation[i].ContiSalp)#,OriginalMWOrder
            for i1 in range(len(SalpPopulation[i].LevelTask)):
                for j1 in range(len(SalpPopulation[i].LevelTask[i1])):
                    random.shuffle(SalpPopulation[i].LevelTask[i1][j1]) # 随机顺序
            SalpPopulation[i] = MateHeuristicIndividual(SalpPopulation[i])
            if NOLOCALSEARCH:
                SalpPopulation[i] = LocalSearch_Salp(SalpPopulation[i])
            # SalpPopulation[i].multiworflow,SalpPopulation[i].VMSchedule,SalpPopulation[i].objectives = MateHeuristicIndividual(SalpPopulation[i].DiscrSalp)
            if time.time() - AlgorithmStart>=1.2*MaxDAGTasks: break
        AlgorithmEnd = time.time()
        AlgorithmRunTime = AlgorithmEnd - AlgorithmStart
        if AlgorithmRunTime>=1.2*MaxDAGTasks: break
    NonDominSalps = NonDominSalps + SalpPopulation  # copy.deepcopy() + copy.deepcopy()
    NonDominSalps = non_dominatedSalps(NonDominSalps,NumNonDominated)   
    NonDominSalps.append(time.time() - AlgorithmStart)
    # return NonDominSalps
    return GlobalResource.RemovePermutation(NonDominSalps)



# app = xw.App(visible=True,add_book=False)
# book = app.books.open('./ResultExcel/testszx.xlsx')
# sheet = book.sheets[0]  #引用工作表   os.getcwd()+  # 'Miscellaneous',

listfileName=os.listdir('./data_npy') #     os.getcwd() data_npy
listfileName.sort()
# listDeadlineFactor = [0.8,1.1,1.5,1.8]

listWorkflowNum = GlobalResource.listWorkflowNum # get_globalvalue('listWorkflowNum')   #  [12,155,139,20,82]  #
# TaotalWfNUm = 5 
# listWorkflowNum= random.sample([i for i in range(len(listfileName))],TaotalWfNUm)
for times in range(1):
    for instance in range(len(listWorkflowNum)):
        # instance = 6
        print('****************\t\t2022_SZX_Three\t Running times=%d \t instance=%d \t\t\t****************'%(times,instance))
        tempmultiWorflow = []
        multiWorflowDeadline = []
        WfDeadline = []
        tempmultiWorflowDAGLevel = []
        MaxDAGTasks = 0
        OriginalMaxDAGTasks = 0
        for n1 in listWorkflowNum[instance][:]:#-3  80, 8,   19-3,
            fileName = listfileName[n1]
            WorkFlowTestName = fileName[0:-4] # len(fileName)-12
            # DeadlineFactor = fileName[len(fileName)-7:len(fileName)-4]
            workflow = np.load(os.getcwd()+'/data_npy/'+fileName,allow_pickle=True).item()
            DeadlineFactor = workflow.pop('DeadlineFactor')   
            Deadline = workflow.pop('Deadline') # ResetDeadline(workflow,DeadlineFactor) 
            # Deadline = Deadline*3
            OriginalMaxDAGTasks += len(workflow) # 总任务数
            '''
            task.MI=1表示具有隐私属性；   task.XFT 为 sub-deadline 
            '''

            case1_Private(workflow)
            DAGLevel = taskTopologicalLevel(workflow)     #DAG分层处理

            getSubDeadline(workflow,Deadline)  # 在此算法中用task.XFT表示Sub-deadline
            WfDeadline.append(Deadline)
            multiWorflowDeadline.append({'Deadline':Deadline,'DeadlineFactor':DeadlineFactor,'WorkflowName':WorkFlowTestName} )
            tempmultiWorflowDAGLevel.append(DAGLevel)
            tempmultiWorflow.append(workflow)
            MaxDAGTasks += len(workflow) # 总任务数
            del workflow

        ## 混合云
        PUBLICID  = 0
        PRIVATEID = 1
        HYBRIDCLOUD = [PUBLICID,PRIVATEID]
        DTT = GlobalResource.DTT #传输时间放大倍数
        VMT = [VMType(),PrivateCloudVMType()]
        tempVMS = [[],[]]
        for cloudID in HYBRIDCLOUD:
            if cloudID==PRIVATEID:
                for i in VMT[cloudID].P:
                    if GlobalResource.NUMofPrivateCloudVM[i]>0:
                        tempVMS[cloudID].append(VMScheduling(VMT[cloudID].P[i], VMT[cloudID].N[i]))
            else:
                for i in VMT[cloudID].P:
                    tempVMS[cloudID].append(VMScheduling(VMT[cloudID].P[i], VMT[cloudID].N[i]))
        MW_Level = [len(eachworkflow) for eachworkflow in tempmultiWorflowDAGLevel] 
        OriginalMWOrder = [i for i in range(len(MW_Level)) for j in range(MW_Level[i])]
        
        
        # ## HSA9Fs  BEGIN
        AlgorithmStart = time.time()
        Salp = HeuristicIndividual()
        AlgorithmEnd = time.time()
        AlgorithmRunTime = AlgorithmEnd - AlgorithmStart   
        # GlobalResource.RemovePermutation(NonDominSalps)  
        # Salp.objectives.AlgorithmRunTime  = AlgorithmRunTime
        Salp = [Salp]
        Salp.append(AlgorithmRunTime)
        Salp = GlobalResource.RemovePermutation(Salp)  
        # gantt_VMState_MultiWorkflow(Salp.VMSchedule,Salp.multiworflow,Salp.objectives)
        str1 = str(instance)+'_'+str(len(listWorkflowNum[instance]))+'_'+str(OriginalMaxDAGTasks)+'_'+str(times) # -'+str1+'
        np.save(os.getcwd()+'/ParetoFront/'+'2022_HSM_NF-'+str1+'.npy', Salp)   
        SuccessfulRate = Salp[0].SuccessfulRate
        print('****************\t\t\t2022_SZX_Three\t End times=%d \t instance=%d \t SuccessfulRate=%f\t\t****************'%(times,instance,SuccessfulRate))   
        # ## HSA9Fs  END


        
        # ##########  MSIA   BEGIN
        # NOLOCALSEARCH = True
        # NonDominSalps = MSSA()
        # str1 = str(instance)+'_'+str(len(listWorkflowNum[instance]))+'_'+str(OriginalMaxDAGTasks)+'_'+str(times) # -'+str1+'
        # np.save(os.getcwd()+'/ParetoFront/'+'2022_SZX_NF-'+str1+'.npy', NonDominSalps)
        # print('****************\t\t\t2022_SZX_Three\t End times=%d \t instance=%d \t\t****************'%(times,instance))
        # ##########  MSIA  END

K = 1 