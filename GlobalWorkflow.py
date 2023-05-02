from sys import maxsize
import matplotlib
import matplotlib.pyplot as plt
from math import trunc
import os

from matplotlib.pyplot import close  

from Class.SyntheticGenerator import SyntheticGenerator
import numpy as np
from Class.VMType import PrivateCloudVMType
import GlobalResource
from Class.File import File
from Class.Task import Task
import math,random
import copy

import xlwings as xw

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

def ResetDeadline(workflow,DeadlineFactor):
    MET = getMET_SubDeadline(workflow)          #  /GlobalResource.maxECU
    EST,EFT = getEST_SubDeadline(workflow,MET)  #  /GlobalResource.maxB
    Deadline = max(EFT)*DeadlineFactor
    return Deadline


class SalpClass:   #  szx
    def __init__(self):
        self.ContiSalp=None
        self.DiscrSalp=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.LevelTask=None
class ChromClass:  #   IS
    def __init__(self):
        self.X=None
        self.Y=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.pm = None
        self.pc = None

class ChromClass:   #  ASC
    def __init__(self):
        """ .TasksOrder 任务序列"""
        self.VMOrder=None
        self.TasksOrder=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.scheduleMatrix=None
        self.cloneVector=None
        self.PBVMIndexlist = None
        self.VMList = None

class ChromClass:  #  IJPR
    def __init__(self):
        """ .TasksOrder 任务序列"""
        self.VMOrder=None
        self.TasksOrder=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
####################  读取非劣解集 .npy文件    ####################################

app = xw.App(visible=True, add_book=False)
app.display_alerts = False    # 关闭一些提示信息，可以加快运行速度。 默认为 True。
app.screen_updating = True    # 更新显示工作表的内容。默认为 True。关闭它也可以提升运行速度。
book = app.books.add()
sheet = book.sheets.active
listfileName=os.listdir(os.getcwd()+'\\ParetoFront') 
PF = []
# for fileName in listfileName:
for n1 in range(len(listfileName)):
    fileName = listfileName[n1]
    tempPF = np.load(os.getcwd()+'\\ParetoFront\\'+fileName,allow_pickle=True)
    PF.append(np.load(os.getcwd()+'\\ParetoFront\\'+fileName,allow_pickle=True)) # ,allow_pickle=True).item()) # 

    for i in range(len(tempPF)):
        sheet[i,n1*3+1].value = str(tempPF[i].objectives.Cost)
        sheet[i,n1*3+2].value = str(tempPF[i].objectives.Energy)
        sheet[i,n1*3+3].value = str(tempPF[i].objectives.TotalTardiness)

k = 1
###############################################################################################


# ####################### 读取  GlobalResource.WorkFlowTestName  数据 存到 .npy文件 ############################################
# syntheticGenerator = SyntheticGenerator('%s.xml'%GlobalResource.WorkFlowTestName) #     

# workflow = syntheticGenerator.generateSyntheticWorkFlow()

# MET = getMET(workflow)
# EST,EFT = getEST(workflow,MET)
# Deadline = max(EFT)

# workflow['Deadline'] = trunc(Deadline*1.1)

# currentpath = os.getcwd()

# np.save(currentpath+'\\data_npy\\'+GlobalResource.WorkFlowTestName+'.npy', workflow)                  #保存字典 注意带上后缀名

# # workflow2 =  np.load(WorkFlowTestName+'.npy',allow_pickle=True).item()   #读取字典

# print('GlobalWorkflow')
# ################################################################################################


####################  读取所有数据 并将字典格式的workflow存到 .npy文件    ####################################
listfileName=os.listdir(r'D:\OneDrive - stu.kust.edu.cn\Ph.D\Procedure\Synthetic Workflows') 
listDeadlineFactor = [0.8,1.1,1.5,1.8] 
PrivateFactor = 4
for fileName in listfileName:    #os.getcwd() 
    if fileName.endswith('.xml') :
        for DeadlineFactor in listDeadlineFactor:
            for factor in range(PrivateFactor):
                print('****************\t\t\t' + fileName + ' is running. \t\t\t****************')
                syntheticGenerator = SyntheticGenerator(fileName) #'%s.xml'% 
                workflow = syntheticGenerator.generateSyntheticWorkFlow()
                for taskid,task in workflow.items():
                    task.runtime = abs(task.runtime*GlobalResource.ReferenceProcessingCapacity)
                    task.MI = 1 if random.random()<0.2 else 0  # random.randint(0,1)  
                Deadline = ResetDeadline(workflow,DeadlineFactor) 
                # DeadlineFactor = 1.1
                workflow['Deadline'] = trunc(Deadline*DeadlineFactor)
                workflow['DeadlineFactor'] = DeadlineFactor
                currentpath = os.getcwd()
                workflowName = fileName[0:5]+'_'+"".join(list(filter(str.isdigit, fileName))).rjust(4,'0')
                np.save(currentpath+'\\data_npy\\'+workflowName+'_'+str(DeadlineFactor)+'_'+str(factor)+'.npy', workflow)                  #保存字典 注意带上后缀名
k = 1
###############################################################################################
