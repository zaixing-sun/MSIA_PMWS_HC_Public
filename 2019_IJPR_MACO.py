'''[1] F. Li, L. Zhang, T. W. Liao, and Y. Liu, “Multi-objective optimisation of multi-task scheduling in cloud manufacturing,” Int. J. Prod. Res., vol. 57, no. 12, pp. 3847–3863, 2019, doi: 10.1080/00207543.2018.1538579.'''
from ast import Assign
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
    return DAGLevel

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
    plt.title("WorkflowScheduling_%s_%.3f_%.3f_%.3f"%(WorkFlowTestName, #GlobalResource. _%s os.path.basename(__file__).split(".")[0],
                                        objectives.Cmax,objectives.Cost,objectives.Energy))
    # plt.title("WorkflowScheduling_%s_%s_%s"%(WorkFlowTestName,DeadlineFactor,os.path.basename(__file__).split(".")[0]))
    # plt.legend(handles=patches,loc=4)
    #XY轴标签
    plt.xlabel("Time/s",fontsize = FontSize)
    plt.ylabel("VM",fontsize = FontSize)    
    #plt.grid(linestyle="--",alpha=0.5)  #网格线
    plt.savefig(".\GanttChart\WorkflowScheduling_%s_%s_%s.png"%(WorkFlowTestName,DeadlineFactor,
        os.path.basename(__file__).split(".")[0]), dpi=300, format='png',bbox_inches="tight")
    plt.show()    # gantt_VMState(VMS)

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
    MET = getMET_SubDeadline(workflow)
    EST,EFT = getEST_SubDeadline(workflow,MET)
    Deadline = max(EFT)*DeadlineFactor
    return Deadline



###########################################################
###########################################################
class ChromClass:
    def __init__(self):
        """ .TasksOrder 任务序列"""
        self.VMOrder=None
        self.TasksOrder=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        # self.SequencePheromone = None
        # self.VMPheromone = None
        # self.pm = None
        # self.pc = None

def ChromosomeInitialization():
    '''初始化'''
    # global PUBLICID,PRIVATEID,multiWorflow,VMS,multiWorflowDAGLevel,LevelMaxFinishTtime,FT_Star,ListLevelVM  # 
    chromosome = ChromClass()
    chromosome.multiworflow = copy.deepcopy(tempmultiWorflow)
    T = []
    for dag in range(len(tempmultiWorflow)):
        for taskid in range(len(tempmultiWorflow[dag])):
            T.append([dag,taskid])
    
    chromosome.TasksOrder = []
    while T!=[]:
        S = []
        for ti in T:            
            nofind = True
            for eachPar in chromosome.multiworflow[ti[0]][ti[1]].inputs:
                if [ti[0],eachPar.id] not in chromosome.TasksOrder:
                    nofind = False
                    break
            if nofind:
                S.append(ti)
        while S != []:            
            randomTask = S.pop(random.randint(0,len(S)-1)) #   []
            T.remove(randomTask)
            chromosome.TasksOrder.append(randomTask)

    # DAG = copy.deepcopy(tempmultiWorflow)
    # T= []
    # for each in range(len(DAG)):        
    #     list1 = [taskId for taskId,task in DAG[each].items()]
    #     DAG[each][len(DAG[each])] = Task(len(DAG[each]),name = 'entry')
    #     T.append([each,len(DAG[each])-1])
    #     for taskId in list1:
    #         T.append([each,taskId])
    #         if DAG[each][taskId].inputs == []:   #原源节点 size = 0  JITCAWorkflow[len(JITCAWorkflow)-1]
    #             tout = File('EntryOut', id = len(DAG[each])-1)
    #             DAG[each][taskId].inputs.append(tout)
    #             tout = File('Entry', id = taskId)
    #             DAG[each][len(DAG[each])-1].addOutput(tout)
    # WFnum = random.randint(0,len(DAG)-1)
    # TNum = DAG[WFnum][len(DAG[WFnum])-1].id

    # chromosome.TasksOrder = [[WFnum,TNum]]
    # T.remove([WFnum,TNum])
    # S = []
    # while T!=[]:
    #     for ti in T:            
    #         nofind = True
    #         for eachPar in DAG[ti[0]][ti[1]].inputs:
    #             if [ti[0],eachPar.id] not in chromosome.TasksOrder:
    #                 nofind = False
    #                 break
    #         if nofind:
    #             S.append(ti)
    #     # ## 更改后
    #     # while S != []:            
    #     #     randomTask = S[random.randint(0,len(S)-1)]
    #     #     T.remove(randomTask)
    #     #     chromosome.TasksOrder.append(randomTask)
    #     #     # S = []
    #     # 更改前
    #     randomTask = S[random.randint(0,len(S)-1)]
    #     T.remove(randomTask)
    #     chromosome.Y.append(randomTask)
    #     S = []

    # for WFnum in range(len(DAG)): 
    #     chromosome.TasksOrder.remove([WFnum,len(DAG[WFnum])-1])
    # del DAG

    for i in range(len(chromosome.multiworflow)):
        for j in range(len(chromosome.multiworflow[i])):
            if chromosome.multiworflow[i][j].MI==PRIVATEID: ## yes
                CloudID = PRIVATEID
                r1 = sum(GlobalResource.NUMofPrivateCloudVM[0:-1])
                VmID = random.randint(0,r1)
            else:
                CloudID = random.choice(HYBRIDCLOUD)
                if CloudID ==PRIVATEID:## yes
                    r1 = sum(GlobalResource.NUMofPrivateCloudVM[0:-1])
                    VmID = random.randint(0,r1)
                else:  ##  yes
                    Vmtype = random.randint(0,VMT[CloudID].m-1)
                    nums = random.randint(0,EachPBVMTypeNums-1)
                    VmID =  EachPBVMTypeNums*Vmtype + nums  # random.randint(0,PBVMNums-1)
            chromosome.multiworflow[i][j].VMnum = [CloudID,VmID]
    chromosome.VMOrder = []
    for y1 in chromosome.TasksOrder:
        chromosome.VMOrder.append(chromosome.multiworflow[y1[0]][y1[1]].VMnum  )
    # chromosome.pm = 1/max( [len(chromosome.multiworflow[i]) for i in range(len(chromosome.multiworflow))])
    # chromosome.pc = 1

    CalcaulateTaskObject_MultiWorkflow(chromosome)
    return chromosome

def InitialPheromoneMatrices(non_dominated_Solution):
    global  Alpha,Beta,Rho,Q1,Q2,PBVMNums,PRVMNums,TaskList
    # TaskList = []
    # for dag in range(len(tempmultiWorflow)):
    #     for taskid in range(len(tempmultiWorflow[dag])):
    #         TaskList.append([dag,taskid])
    InitialPheromone = 10 
    VMPheromone = []
    for dag in range(len(tempmultiWorflow)):
        VMPheromone.append([])
        for taskid in range(len(tempmultiWorflow[dag])):
            VMPheromone[dag].append([])
            for obj in range(3):  ### obj =0时表示花费 1时表示能耗  1是私有云
                VMPheromone[dag][taskid].append([])
                for cloudid in HYBRIDCLOUD:
                    VMPheromone[dag][taskid][obj].append([])
                    if cloudid == PRIVATEID:
                        for VMid in range(PRVMNums):
                            tempQ = 0
                            for chrome1  in non_dominated_Solution:
                                if chrome1.multiworflow[dag][taskid].VMnum ==[cloudid,VMid]:
                                    # tempQ = Q1/chrome1.objectives.Cost if obj==0 else Q1/chrome1.objectives.Energy
                                    if obj==0:
                                        tempQ = Q1/chrome1.objectives.Cost
                                    elif obj==1:
                                        tempQ = Q1/chrome1.objectives.Energy
                                    else:
                                        tempQ = Q1/(chrome1.objectives.TotalTardiness+0.0001)
                                    break
                            VMPheromone[dag][taskid][obj][cloudid].append( (1-Rho)*InitialPheromone+ tempQ)
                    elif cloudid==PUBLICID:
                        if tempmultiWorflow[dag][taskid].MI==PRIVATEID:
                            for VMid in range(PBVMNums):
                                VMPheromone[dag][taskid][obj][cloudid].append( 0)
                        else:
                            for VMid in range(PBVMNums):
                                tempQ = 0
                                for chrome1  in non_dominated_Solution:
                                    if chrome1.multiworflow[dag][taskid].VMnum ==[cloudid,VMid]:
                                        if obj==0:
                                            tempQ = Q1/chrome1.objectives.Cost
                                        elif obj==1:
                                            tempQ = Q1/chrome1.objectives.Energy
                                        else:
                                            tempQ = Q1/(chrome1.objectives.TotalTardiness+0.0001)
                                        break
                                VMPheromone[dag][taskid][obj][cloudid].append( (1-Rho)*InitialPheromone+ tempQ)                            

    SequencePheromone = []
    SequencePheromone0 = []
    for b in range(2):
        SequencePheromone.append([])        
        for i in range(len(TaskList)):
            SequencePheromone[b].append([])
            preTask = TaskList[i]
            for j in range(len(TaskList)): 
                sucTask = TaskList[j]
                tempQ = 0
                for chrome1 in non_dominated_Solution:
                    preIndex = chrome1.TasksOrder.index(preTask)
                    sucIndex = chrome1.TasksOrder.index(sucTask)
                    if preIndex+1 ==sucIndex:
                        tempQ = Q1/chrome1.objectives.Cost if b==0 else Q1/chrome1.objectives.Energy 
                        # if obj==0:
                        #     tempQ = Q1/chrome1.objectives.Cost
                        # elif obj==1:
                        #     tempQ = Q1/chrome1.objectives.Energy
                        # else:
                        #     tempQ = Q1/(chrome1.objectives.TotalTardiness+0.0001)                        
                        break      
                SequencePheromone[b][i].append((1-Rho)*InitialPheromone+ tempQ)        
        SequencePheromone0.append([])
        for i in range(len(TaskList)):
            preTask = TaskList[i]
            tempQ = 0
            for chrome1 in non_dominated_Solution:
                if chrome1.TasksOrder[0] ==preTask:
                    tempQ = Q1/chrome1.objectives.Cost if b==0 else Q1/chrome1.objectives.Energy 
                    # if obj==0:
                    #     tempQ = Q1/chrome1.objectives.Cost
                    # elif obj==1:
                    #     tempQ = Q1/chrome1.objectives.Energy
                    # else:
                    #     tempQ = Q1/(chrome1.objectives.TotalTardiness+0.0001)                    
                    break       
            SequencePheromone0[b].append((1-Rho)*InitialPheromone+ tempQ) 

    return VMPheromone,SequencePheromone,SequencePheromone0

def updatePheromoneMatrices(non_dominated_Solution,VMPheromone,SequencePheromone,SequencePheromone0):
    global  Alpha,Beta,Rho,Q1,Q2,PBVMNums,PRVMNums,TaskList

    for dag in range(len(tempmultiWorflow)):
        for taskid in range(len(tempmultiWorflow[dag])):
            for obj in range(3):  ### obj =0时表示花费 1时表示能耗  1是私有云
                for cloudid in HYBRIDCLOUD:
                    if cloudid == PRIVATEID:
                        for VMid in range(PRVMNums):
                            tempQ = 0
                            for chrome1  in non_dominated_Solution:
                                if chrome1.multiworflow[dag][taskid].VMnum ==[cloudid,VMid]:
                                    # tempQ = Q1/chrome1.objectives.Cost if obj==0 else Q1/chrome1.objectives.Energy 
                                    if obj==0:
                                        tempQ = Q1/chrome1.objectives.Cost
                                    elif obj==1:
                                        tempQ = Q1/chrome1.objectives.Energy
                                    else:
                                        tempQ = Q1/(chrome1.objectives.TotalTardiness+0.0001)                                    
                                    break
                            VMPheromone[dag][taskid][obj][cloudid][VMid] =  (1-Rho)*VMPheromone[dag][taskid][obj][cloudid][VMid]+ tempQ
                    elif cloudid==PUBLICID:
                        if tempmultiWorflow[dag][taskid].MI==PRIVATEID:
                            for VMid in range(PBVMNums):
                                VMPheromone[dag][taskid][obj][cloudid][VMid] =0
                        else:
                            for VMid in range(PBVMNums):
                                tempQ = 0
                                for chrome1  in non_dominated_Solution:
                                    if chrome1.multiworflow[dag][taskid].VMnum ==[cloudid,VMid]:
                                        # tempQ = Q1/chrome1.objectives.Cost if obj==0 else Q1/chrome1.objectives.Energy 
                                        if obj==0:
                                            tempQ = Q1/chrome1.objectives.Cost
                                        elif obj==1:
                                            tempQ = Q1/chrome1.objectives.Energy
                                        else:
                                            tempQ = Q1/(chrome1.objectives.TotalTardiness+0.0001)                                        
                                        break
                                VMPheromone[dag][taskid][obj][cloudid][VMid] =  (1-Rho)*VMPheromone[dag][taskid][obj][cloudid][VMid]+ tempQ                            

    # SequencePheromone = []
    # SequencePheromone0 = []
    for b in range(2):   
        for i in range(len(TaskList)):
            preTask = TaskList[i]
            for j in range(len(TaskList)): 
                sucTask = TaskList[j]
                tempQ = 0
                for chrome1 in non_dominated_Solution:
                    preIndex = chrome1.TasksOrder.index(preTask)
                    sucIndex = chrome1.TasksOrder.index(sucTask)
                    if preIndex+1 ==sucIndex:
                        tempQ = Q1/chrome1.objectives.Cost if b==0 else Q1/chrome1.objectives.Energy 
                        if obj==0:
                            tempQ = Q1/chrome1.objectives.Cost
                        elif obj==1:
                            tempQ = Q1/chrome1.objectives.Energy
                        else:
                            tempQ = Q1/(chrome1.objectives.TotalTardiness+0.0001)                        
                        break      
                SequencePheromone[b][i][j]= (1-Rho)*SequencePheromone[b][i][j]+ tempQ       

        for i in range(len(TaskList)):
            preTask = TaskList[i]
            tempQ = 0
            for chrome1 in non_dominated_Solution:
                if chrome1.TasksOrder[0] ==preTask:
                    tempQ = Q1/chrome1.objectives.Cost if b==0 else Q1/chrome1.objectives.Energy 
                    # if obj==0:
                    #     tempQ = Q1/chrome1.objectives.Cost
                    # elif obj==1:
                    #     tempQ = Q1/chrome1.objectives.Energy
                    # else:
                    #     tempQ = Q1/(chrome1.objectives.TotalTardiness+0.0001)                    
                    break       
            SequencePheromone0[b][i] = (1-Rho)*SequencePheromone0[b][i]+ tempQ

    return VMPheromone,SequencePheromone,SequencePheromone0

def InitialLambda(popsize):
    global  TotalTasks
    # VMLambda,TaskLambda
    VMLambda = [[random.random() for i in range(popsize)] for q in range(3)]
    for q in range(3):
        sum1 = sum(VMLambda[q])
        for i in range(popsize):
            VMLambda[q][i] = VMLambda[q][i]/sum1
    TaskLambda = [[],[]]        
    for i in range(TotalTasks):
        TaskLambda[0].append(i/TotalTasks)
        TaskLambda[1].append(1-i/TotalTasks)
    return VMLambda,TaskLambda

def generate_VM_Probility(VMPheromone,VMLambda):
    global  Alpha,Beta,Rho,Q1,Q2,PBVMNums,PRVMNums,TaskList,VMList
    VMProbility = []
    for dag in range(len(tempmultiWorflow)):
        VMProbility.append([])
        for taskid in range(len(tempmultiWorflow[dag])):
            VMProbility[dag].append([])
            for cloudid in HYBRIDCLOUD:
                VMProbility[dag][taskid].append([])
                for VMid in range(len(tempVMS[cloudid])):
                    t1 = 1 
                    for obj in range(3):
                        t1 = t1*math.pow(VMPheromone[dag][taskid][obj][cloudid][VMid],VMLambda[obj])
                    t1 = math.pow(t1,Alpha)
                    t2 = 1 
                    taskRunTime = (tempmultiWorflow[dag][taskid].runtime/VMT[cloudid].ProcessingCapacity[tempVMS[cloudid][VMid].id])
                    t2 = t2 * math.pow(1/taskRunTime,VMLambda[1]) * math.pow(1/taskRunTime,VMLambda[2])
                    if cloudid==PUBLICID:
                        taskCost = taskRunTime* VMT[cloudid].M[tempVMS[cloudid][VMid].id] /3600
                        t2 = t2 * math.pow(1/taskCost,VMLambda[0])
                    t2 = math.pow(t2,Beta)
                    Numerator = t1 * t2  ##  分子
                    Denominator = 0        #  分母
                    for vm in range(len(VMList)):
                        cid = VMList[vm][0]
                        Vid = VMList[vm][1]
                        t1 = 1 
                        for obj in range(3):
                            t1 = t1*math.pow(VMPheromone[dag][taskid][obj][cid][Vid],VMLambda[obj])
                        t1 = math.pow(t1,Alpha)
                        t2 = 1 
                        taskRunTime = (tempmultiWorflow[dag][taskid].runtime/VMT[cid].ProcessingCapacity[tempVMS[cid][Vid].id])
                        t2 = t2 * math.pow(1/taskRunTime,VMLambda[1]) * math.pow(1/taskRunTime,VMLambda[2])
                        if cid==PUBLICID:
                            taskCost = taskRunTime* VMT[cid].M[tempVMS[cid][Vid].id] /3600
                            t2 = t2 * math.pow(1/taskCost,VMLambda[0])
                        t2 = math.pow(t2,Beta)
                        Denominator = Denominator + t1 * t2  ##  分子   
                    VMProbility[dag][taskid][cloudid].append(Numerator/Denominator) 
    return VMProbility

def AssignVM(VMProbility):
    global  TaskList,VMList
    # VMIndexOrder,VMorder
    VMIndexOrder = []
    for i in  range(len(TaskList)):
        dag = TaskList[i][0]
        taskid = TaskList[i][1]
        Probility = []
        for j in VMList:
            if (tempmultiWorflow[dag][taskid].MI==PRIVATEID)and (j[0]!=PRIVATEID)and(VMProbility[dag][taskid][j[0]][j[1]]!=0):
                kkkkkkk = 0


            Probility.append(VMProbility[dag][taskid][j[0]][j[1]] )
        # while True:
        sumP = sum(Probility) 
        rand1 = sumP* random.random()        
        index = 0
        sum1 = Probility[index]
        while True:
            if (sum1<rand1):
                sum1 = sum1 + Probility[index]
                index += 1
            else:
                if index ==len(VMList):
                    index = Probility.index(max(Probility))
                break
        VMIndexOrder.append(index)
        if (tempmultiWorflow[dag][taskid].MI==PRIVATEID)and (VMList[index][0]!=PRIVATEID):
            kkkkkkk = 0
            # elif (tempmultiWorflow[dag][taskid].MI!=PRIVATEID):
            #     VMIndexOrder.append(index)
            #     break
    VMorder = [VMList[i] for i in VMIndexOrder] 
    return VMorder # VMIndexOrder,


def generate_Task_Probility_taskorder(SequencePheromone,SequencePheromone0,TaskLambda):
    '''无设置时间，将式（18）中的设置时间和设置成本 赋值为1'''
    global  Alpha,Beta,Rho,Q1,Q2,PBVMNums,PRVMNums,TaskList,VMList

    TaskProbility0 = []
    for i in range(len(TaskList)):
        Numerator = 1 
        for obj in range(2):
            Numerator = Numerator * math.pow(SequencePheromone0[obj][i],TaskLambda[obj])
        Numerator = math.pow(Numerator,Alpha)    
        Denominator = 0
        for j in range(len(TaskList)):
            t1 = 1 
            for obj in range(2):
                t1 = t1 * math.pow(SequencePheromone0[obj][j],TaskLambda[obj])
            t1 = math.pow(t1,Alpha) 
            Denominator = Denominator + t1
        TaskProbility0.append(Numerator/Denominator)


    taskIndexOrder = []
    rand1 = sum(TaskProbility0) * random.random()    
    index = 0
    sum1 = TaskProbility0[index]
    while True:
        if sum1<rand1:
            sum1 = sum1 + TaskProbility0[index]
            index += 1
        else:
            if index ==len(VMList):
                index = TaskProbility0.index(max(TaskProbility0))            
            break
    taskIndexOrder.append(index)
    preIndex = index

    for kk in range(1,len(TaskList)):
        TaskProbility = []
        for i in range(len(TaskList)):
            if i in set(taskIndexOrder):
                TaskProbility.append(0)
                continue
            Numerator = 1 
            for obj in range(2):
                Numerator = Numerator * math.pow(SequencePheromone[obj][preIndex][i],TaskLambda[obj])
            Numerator = math.pow(Numerator,Alpha)    
            Denominator = 0
            for j in range(len(TaskList)):
                t1 = 1 
                for obj in range(2):
                    t1 = t1 * math.pow(SequencePheromone[obj][preIndex][j],TaskLambda[obj])
                t1 = math.pow(t1,Alpha) 
                Denominator = Denominator + t1
            TaskProbility.append(Numerator/Denominator)  

        sumP = sum(TaskProbility)
        rand1 = sumP * random.random()  
        index = 0
        sum1 = TaskProbility[index]
        while True:
            if (sum1<rand1)or (index in taskIndexOrder):
                sum1 = sum1 + TaskProbility[index]
                index += 1
            else:
                if index ==len(TaskList):
                    index = TaskProbility.index(max(TaskProbility))
                break
        taskIndexOrder.append(index)
        preIndex = index


    taskorder = [TaskList[index]  for index in taskIndexOrder   ]
    # taskIndexOrder.sort()
    taskorder = sequenceAdjustment(taskorder)
    return taskorder # taskIndexOrder,

def sequenceAdjustment(taskorder):
    global  Alpha,Beta,Rho,Q1,Q2,PBVMNums,PRVMNums,TaskList,VMList
    newtaskorder = []
    for i in range(len(taskorder)):
        dag = taskorder[i][0]
        taskid = taskorder[i][1]        
        if tempmultiWorflow[dag][taskid].inputs==[]:
            newtaskorder.append(taskorder[i])
    for i in newtaskorder:
        taskorder.pop(taskorder.index(i))
    while taskorder!=[]:
        for i in range(len(taskorder)):
            dag = taskorder[i][0]
            taskid = taskorder[i][1]
            nofind = True
            for pre in tempmultiWorflow[dag][taskid].inputs:
                if [dag,pre.id] not in newtaskorder:
                    nofind = False
                    break
            if nofind:
                newtaskorder.append(taskorder.pop(i))
                break
    return newtaskorder


def generate_Calcaulate_ant(taskorder,VMorder):
    global  Alpha,Beta,Rho,Q1,Q2,PBVMNums,PRVMNums,TaskList,VMList
    chromosome = ChromClass()
    chromosome.multiworflow = copy.deepcopy(tempmultiWorflow)
    chromosome.VMOrder = VMorder[:]
    chromosome.TasksOrder = taskorder[:]
    for i in range(len(VMorder)):
        dag = TaskList[i][0]
        taskid = TaskList[i][1]
        chromosome.multiworflow[dag][taskid].VMnum = VMorder[i]
    CalcaulateTaskObject_MultiWorkflow(chromosome)
    return chromosome

def CalcaulateTaskObject_MultiWorkflow(chromosome):
    chromosome.VMSchedule = copy.deepcopy(tempVMS)
    for i in chromosome.TasksOrder:
        WfID = i[0]
        taskID = i[1]
        vmn = chromosome.multiworflow[WfID][taskID].VMnum
        # task = chromosome.multiworflow[WfID][taskID]
        # TaskST TaskFT TaskEST VmST VmFt
        TaskEST = 0 #  max( [ chromosome.multiworflow[WfID][parentNode.id].FinishTime      ])
        for parentNode in chromosome.multiworflow[WfID][taskID].inputs:
            tempST = chromosome.multiworflow[WfID][parentNode.id].FinishTime
            PNodeVM = chromosome.multiworflow[WfID][parentNode.id].VMnum          
            if PNodeVM != vmn:
                DataTransferRate = min(VMT[vmn[0]].B[chromosome.VMSchedule[vmn[0]][vmn[1]].id], VMT[PNodeVM[0]].B[chromosome.VMSchedule[PNodeVM[0]][PNodeVM[1]].id])
                DataTransferTime = (parentNode.size/DataTransferRate * DTT)
            else:
                DataTransferTime = 0
            
            if TaskEST<tempST+DataTransferTime:
                TaskEST = tempST+DataTransferTime
        taskcore = 0
        VmST = chromosome.VMSchedule[vmn[0]][vmn[1]].CompleteTime[taskcore]
        chromosome.multiworflow[WfID][taskID].StartTime = max(TaskEST,VmST)
        chromosome.multiworflow[WfID][taskID].FinishTime = chromosome.multiworflow[WfID][taskID].StartTime + (chromosome.multiworflow[WfID][taskID].runtime/VMT[vmn[0]].ProcessingCapacity[chromosome.VMSchedule[vmn[0]][vmn[1]].id])
        
        chromosome.VMSchedule[vmn[0]][vmn[1]].CompleteTime[taskcore] = chromosome.multiworflow[WfID][taskID].FinishTime
        chromosome.VMSchedule[vmn[0]][vmn[1]].TaskCore[taskcore].insert(len(chromosome.VMSchedule[vmn[0]][vmn[1]].TaskCore[taskcore]),i) 

        list1 = [chromosome.multiworflow[WfID][taskID].StartTime,chromosome.multiworflow[WfID][taskID].FinishTime] 
        chromosome.VMSchedule[vmn[0]][vmn[1]].VMTime[taskcore].insert(len(chromosome.VMSchedule[vmn[0]][vmn[1]].VMTime[taskcore]),list1)        
    chromosome.objectives = GlobalResource.caculateMultiWorkflowMakespan_Cost(chromosome.multiworflow,WfDeadline,chromosome.VMSchedule)
    # gantt_VMState_MultiWorkflow(chromosome.VMSchedule,chromosome.multiworflow,chromosome.objectives)


# def DetermineWhether2Dominate(salpA,salpB): ## Cost   Energy
#     ''' salpA 可支配 salpB  '''
#     if ((salpA.objectives.Cost<=salpB.objectives.Cost) and(salpA.objectives.Energy<=salpB.objectives.Energy)):
#         # return True  # 包含相等的
#         if ((salpA.objectives.Cost<salpB.objectives.Cost) or (salpA.objectives.Energy<salpB.objectives.Energy)):
#             return True
#     return False


def fast_non_dominated_sort(Population):
    ## values1,values2
    S = [[] for i in range(len(Population))]
    front = [[]]
    n = [0 for i in range(len(Population))]
    rank = [0 for i in range(len(Population))]
    for p in range(len(Population)):
        S[p] = []
        n[p] = 0
        for q in range(len(Population)):
            if GlobalResource.DetermineWhether2Dominate(Population[p],Population[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif GlobalResource.DetermineWhether2Dominate(Population[q],Population[p]):
                n[p] = n[p] + 1
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    i = 0
    while(front[i] != []):
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if (n[q] == 0):
                    rank[q] = i+1
                    if q not in Q:
                        Q.append(q)
        i += 1
        front.append(Q)
    del front[len(front) -1]
    return front

def crowding_distance(Population,front):
    crowding_distance = []
    for each in range(len(front)):
        distance = [0 for i in range(len(front[each]))]
        values1 = [Population[i].objectives.Cost   for i in front[each]] 
        values2 = [Population[i].objectives.Energy  for i in front[each]]
        values3 = [Population[i].objectives.TotalTardiness for i in front[each]]
        # maxTardiness,minTardiness = max(listTardiness),min(listTardiness)
        temp = [[i,Population[i].objectives.Cost] for i in front[each]]
        temp = sorted(temp, key=lambda temp: temp[1]) 
        sorted1 = [ temp[i][0] for i in range(len(front[each]))]
        # sorted1 = sort_by_values(front[each],values1[:])  ###  返回的是索引
        # sorted2 = sort_by_values(front[each],values2[:])
        
        distance[front[each].index(sorted1[0])] = inf
        distance[front[each].index(sorted1[len(front[each]) - 1])] = inf
        for k in range(1,len(front[each])-1):
            dk = front[each].index(sorted1[k])
            dk1 = front[each].index(sorted1[k+1])
            dk0 = front[each].index(sorted1[k-1])            
            if (max(values1)!=min(values1)):
                distance[dk] = distance[dk]+abs(values1[dk1]-values1[dk0])/(max(values1)-min(values1))
            if (max(values2)!=min(values2)):
                distance[dk] = distance[dk]+abs(values2[dk1]-values2[dk0])/(max(values2)-min(values2))
            if (max(values3)!=min(values3)):
                distance[dk] = distance[dk]+abs(values3[dk1]-values3[dk0])/(max(values3)-min(values3))

        # if (max(values1)==min(values1))and((max(values2)!=min(values2))):
        #     for k in range(1,len(front[each])-1):
        #         dk = front[each].index(sorted1[k])
        #         dk1 = front[each].index(sorted1[k+1])
        #         dk0 = front[each].index(sorted1[k-1])
        #         distance[dk] =distance[dk]+abs(values2[dk1]-values2[dk0])/(max(values2)-min(values2))        
        # elif (max(values1)!=min(values1))and((max(values2)==min(values2))):
        #     for k in range(1,len(front[each])-1):
        #         dk = front[each].index(sorted1[k])
        #         dk1 = front[each].index(sorted1[k+1])
        #         dk0 = front[each].index(sorted1[k-1])
        #         distance[dk] = distance[dk]+abs(values1[dk1]-values1[dk0])/(max(values1)-min(values1))  
        # elif (max(values1)!=min(values1))and((max(values2)!=min(values2))):
        #     for k in range(1,len(front[each])-1):
        #         dk = front[each].index(sorted1[k])
        #         dk1 = front[each].index(sorted1[k+1])
        #         dk0 = front[each].index(sorted1[k-1])
        #         distance[dk] =( distance[dk]+abs(values1[dk1]-values1[dk0])/(max(values1)-min(values1)) 
        #                                     +abs(values2[dk1]-values2[dk0])/(max(values2)-min(values2)))
        
        crowding_distance.append(distance)
    return crowding_distance


def crossover_twoPoint(salpA,salpB):   
    global  TaskList,VMList
    NewsalpA = copy.deepcopy(salpA)
    NewsalpB = copy.deepcopy(salpB)

    a1 = random.randint(1,len(salpA.TasksOrder)-2)
    a2 = random.randint(1,len(salpA.TasksOrder)-2)
    while a1==a2:
        a2 = random.randint(1,len(salpA.TasksOrder)-2)
    if a1>a2: 
        a1,a2 = a2,a1
    Order1 = salpA.TasksOrder[a1:a2+1]
    NewsalpA.TasksOrder = []    
    for i in range(len(salpA.TasksOrder)):
        if salpB.TasksOrder[i] not in Order1:
            NewsalpA.TasksOrder.append(salpB.TasksOrder[i])
            if len(NewsalpA.TasksOrder)==a1:
                NewsalpA.TasksOrder = NewsalpA.TasksOrder+salpA.TasksOrder[a1:a2+1]
        else:
            Order1.remove(salpB.TasksOrder[i])
    Order1 = salpB.TasksOrder[a1:a2+1]
    NewsalpB.TasksOrder = []    
    for i in range(len(salpB.TasksOrder)):
        if salpA.TasksOrder[i] not in Order1:
            NewsalpB.TasksOrder.append(salpA.TasksOrder[i])
            if len(NewsalpB.TasksOrder)==a1:
                NewsalpB.TasksOrder = NewsalpB.TasksOrder+salpB.TasksOrder[a1:a2+1]
        else:
            Order1.remove(salpA.TasksOrder[i])
    NewsalpA.TasksOrder = sequenceAdjustment(NewsalpA.TasksOrder)
    NewsalpB.TasksOrder = sequenceAdjustment(NewsalpB.TasksOrder)

    # VMorderA = [salpA.VMOrder[TaskList.index(i) ] for i in salpA.TasksOrder]
    # VMorderB = [salpB.VMOrder[TaskList.index(i) ] for i in salpB.TasksOrder]
    # a1 = random.randint(1,len(salpA.TasksOrder)-2)
    # a2 = random.randint(1,len(salpA.TasksOrder)-2)
    # while a1==a2:
    #     a2 = random.randint(1,len(salpA.TasksOrder)-2)
    # if a1>a2: 
    #     a1,a2 = a2,a1
    # Order1 = VMorderA[a1:a2+1]
    # NewVMorderB = []    
    # for i in range(len(VMorderA)):
    #     if VMorderB[i] not in Order1:
    #         NewVMorderB.append(VMorderB[i])
    #         if len(NewVMorderB)==a1:
    #             NewVMorderB = NewVMorderB+VMorderA[a1:a2+1]
    #     else:
    #         Order1.remove(VMorderB[i])
    #     if len(NewVMorderB)==len(VMorderA): break
    # Order1 = VMorderB[a1:a2+1]
    # NewVMorderA = []    
    # for i in range(len(VMorderB)):
    #     if VMorderA[i] not in Order1:
    #         NewVMorderA.append(VMorderA[i])
    #         if len(NewVMorderA)==a1:
    #             NewVMorderA = NewVMorderA+VMorderB[a1:a2+1]
    #     else:
    #         Order1.remove(VMorderA[i])
    #     if len(NewVMorderA)==len(VMorderA): break
    # VMorderA = [NewVMorderA[salpA.TasksOrder.index(i) ] for i in TaskList]
    # VMorderB = [NewVMorderB[salpB.TasksOrder.index(i) ] for i in TaskList]
    
    # for i in range(len(TaskList)):
    #     dag = TaskList[i][0]
    #     taskid = TaskList[i][1]        
    #     if (tempmultiWorflow[dag][taskid].MI==PRIVATEID):    
    #         if  VMorderA[i][0]!=PRIVATEID:
    #             VMorderA[i] = salpA.VMOrder[i]
    #         if  VMorderB[i][0]!=PRIVATEID:
    #             VMorderB[i] = salpB.VMOrder[i]
    # NewsalpA.VMOrder = VMorderA[:]
    # NewsalpB.VMOrder = VMorderB[:]

    for i in range(len(TaskList)):
        if random.random()>0.5:
            NewsalpA.VMOrder[i] = salpB.VMOrder[i]
            NewsalpB.VMOrder[i] = salpA.VMOrder[i]

    NewsalpA.multiworflow = copy.deepcopy(tempmultiWorflow)
    NewsalpB.multiworflow = copy.deepcopy(tempmultiWorflow)
    for i in range(len(salpA.VMOrder)):
        y1 = NewsalpA.TasksOrder[i] 
        NewsalpA.multiworflow[y1[0]][y1[1]].VMnum = NewsalpA.VMOrder[i]
        y1 = NewsalpB.TasksOrder[i] 
        NewsalpB.multiworflow[y1[0]][y1[1]].VMnum = NewsalpB.VMOrder[i]
    CalcaulateTaskObject_MultiWorkflow(NewsalpA)
    CalcaulateTaskObject_MultiWorkflow(NewsalpB)
    del salpA,salpB
    return NewsalpA,NewsalpB

def mutation(salpA):  # ,salpB
    a1 = random.randint(0,len(salpA.TasksOrder)-1)
    a2 = random.randint(0,len(salpA.TasksOrder)-1)
    while a1==a2:
        a2 = random.randint(0,len(salpA.TasksOrder)-1)
    salpA.TasksOrder[a1],salpA.TasksOrder[a2] = salpA.TasksOrder[a2],salpA.TasksOrder[a1]
    salpA.TasksOrder = sequenceAdjustment(salpA.TasksOrder)

    if random.random()>0.5:
        a1 = random.randint(0,len(salpA.TasksOrder)-1)
        dag = TaskList[a1][0]
        taskid = TaskList[a1][1]

        if salpA.multiworflow[dag][taskid].MI==PRIVATEID: ## yes
            CloudID = PRIVATEID
            r1 = sum(GlobalResource.NUMofPrivateCloudVM[0:-1])
            VmID = random.randint(0,r1)
        else:
            CloudID = random.choice(HYBRIDCLOUD)
            if CloudID ==PRIVATEID:## yes
                r1 = sum(GlobalResource.NUMofPrivateCloudVM[0:-1])
                VmID = random.randint(0,r1)
            else:  ##  yes
                Vmtype = random.randint(0,VMT[CloudID].m-1)
                nums = random.randint(0,EachPBVMTypeNums-1)
                VmID =  EachPBVMTypeNums*Vmtype + nums  # random.randint(0,PBVMNums-1)
        salpA.multiworflow[dag][taskid].VMnum = [CloudID,VmID]
        salpA.VMOrder[a1] = [CloudID,VmID]

    CalcaulateTaskObject_MultiWorkflow(salpA)
    return salpA 

def select(front,distance):
    level = len(front)
    listP0 = [ math.cos(0.5* i/level*math.pi)  for i in range(level)]
    listP = [i/sum(listP0) for i in listP0]
    r1 = random.random()
    ki = 0
    kp = listP[ki]    
    while True:
        if kp>r1:
            select1_level = ki
            break
        else:
            ki += 1
            kp += listP[ki]       
    r1 = random.random()
    ki = 0
    kp = listP[ki]    
    while True:
        if kp>r1:
            select2_level = ki
            if (len(distance[select1_level])==1) and(select1_level == select2_level):
                r1 = random.random()
                ki = 0
                kp = listP[ki]    
                continue             
            else:
                break
        else:
            ki += 1
            kp += listP[ki]

    if (select1_level == select2_level)and(len(distance[select1_level])==2):
        select1_position = 0
        select2_position = 1
    elif(select1_level == select2_level)and(len(distance[select1_level])>2):
        temp = [] # [distance[select1_level][i]  for i in range(len(distance[select1_level]))]
        m1 = []
        for i in range(len(distance[select1_level])):
            if distance[select1_level][i]!=inf:
                m1.append(distance[select1_level][i])
        for i in range(len(distance[select1_level])):
            if distance[select1_level][i]==inf:
                temp.append(max(m1)+min(m1))
            else:
                temp.append(distance[select1_level][i])
        listP = [i/sum(temp) for i in temp]

        r1 = random.random()
        ki = 0
        kp = listP[ki]    
        while True:
            if kp>r1:
                select1_position = ki
                break
            else:
                ki += 1
                kp += listP[ki]       
        r1 = random.random()
        ki = 0
        kp = listP[ki]    
        while True:
            if kp>r1:
                select2_position = ki
                if (select1_position == select2_position):
                    r1 = random.random()
                    ki = 0
                    kp = listP[ki]    
                    continue             
                else:
                    break
            else:
                ki += 1
                kp += listP[ki]
    else:
        select1_position = random.randint(0,len(distance[select1_level])-1)
        select2_position = random.randint(0,len(distance[select2_level])-1)
    return front[select1_level][select1_position],front[select2_level][select2_position]

def updatePopulation(front,distance,Population,popsize):
    for level in range(len(front)):
        temp = []
        for i in range(len(front[level])):
            temp.append([front[level][i],distance[level][i]])            
        temp = sorted(temp, key=lambda temp: temp[1])
        front[level] = [temp[i][0] for i in range(len(temp))]
    # newPopulation = [] 
    # kk = 0
    # for level in range(len(front)):
    #     for i in range(len(front[level])):        
    #         newPopulation.append(Population[front[level][i]]) 
    #         kk += 1
    #         if kk== popsize: break
    #     if kk== popsize: break
    newPopulation = []
    objList = []
    kk = 0
    for level in range(len(front)):
        for i in range(len(front[level])): # ((salpA.objectives.Cost<=salpB.objectives.Cost) and(salpA.objectives.Energy<=salpB.objectives.Energy))
            if (len(newPopulation)>0):
                if [Population[front[level][i]].objectives.Cost,Population[front[level][i]].objectives.Energy,Population[front[level][i]].objectives.TotalTardiness] not in objList:
                # if ((newPopulation[len(newPopulation)-1].objectives.Cost!=Population[front[level][i]].objectives.Cost)and
                #     (newPopulation[len(newPopulation)-1].objectives.Energy!=Population[front[level][i]].objectives.Energy)):
                    newPopulation.append(Population[front[level][i]]) 
                    objList.append([newPopulation[len(newPopulation)-1].objectives.Cost,newPopulation[len(newPopulation)-1].objectives.Energy,newPopulation[len(newPopulation)-1].objectives.TotalTardiness])
                    kk += 1
            else:
                newPopulation.append(Population[front[level][i]])
                objList.append([newPopulation[len(newPopulation)-1].objectives.Cost,newPopulation[len(newPopulation)-1].objectives.Energy,newPopulation[len(newPopulation)-1].objectives.TotalTardiness]) 
                kk += 1
            if kk== popsize: break
        if kk== popsize: break       
    return newPopulation

def MACO(): 
    global  Alpha,Beta,Rho,Q1,Q2,TotalTasks,TaskList,VMList    #  OriginalMWOrder
    
    TotalTasks = sum([len(tempmultiWorflow[i]) for i in range(len(tempmultiWorflow))])  
    popsize = 100  #  math.trunc(1.5*TotalTasks)
    max_iter = 3*TotalTasks 
    Alpha,Beta,Rho,Q1,Q2 = 1,10,0.2,10,0.1
    SequencePheromone = None
    VMPheromone = None    
    AlgorithmStart = time.time()
    TaskList = []
    for dag in range(len(tempmultiWorflow)):
        for taskid in range(len(tempmultiWorflow[dag])):
            TaskList.append([dag,taskid])
    VMList = []
    for cloudid in range(len(tempVMS)):
        for VMid in range(len(tempVMS[cloudid])):
            VMList.append([cloudid,VMid])
    VMLambda,TaskLambda = InitialLambda(popsize)

    Population = [ChromosomeInitialization() for g in range(popsize)]
    non_dominated_sorted_solution = fast_non_dominated_sort(Population)
    non_dominated_Solution = [Population[i] for i in non_dominated_sorted_solution[0]]
    # print('****************\t1\t\t' + str(time.time() - AlgorithmStart) + ' \t\t\t****************')
    # CrowdingDistance = crowding_distance(Population,non_dominated_sorted_solution)
    # Population = updatePopulation(non_dominated_sorted_solution,CrowdingDistance,Population,popsize)
    VMPheromone,SequencePheromone,SequencePheromone0 = InitialPheromoneMatrices(Population)
    # print('****************\t2\t\t' + str(time.time() - AlgorithmStart) + ' \t\t\t****************')
    for iter in range(max_iter):
        Population = []
        for g in range(popsize):
            chromosome = ChromClass()
            chromosome.multiworflow = copy.deepcopy(tempmultiWorflow)            
            antTaskLambda = [TaskLambda[0][g],TaskLambda[1][g]]
            taskorder = generate_Task_Probility_taskorder(SequencePheromone,SequencePheromone0,antTaskLambda) # taskIndexOrder,
            antVMLambda = [VMLambda[0][g],VMLambda[1][g],VMLambda[2][g]]
            VMProbility = generate_VM_Probility(VMPheromone,antVMLambda)
            VMorder = AssignVM(VMProbility) # VMIndexOrder,
            Population.append(generate_Calcaulate_ant(taskorder,VMorder))
            # print('****************\t3\t\t' + str(time.time() - AlgorithmStart) + ' \t\t\t****************')
            if time.time() - AlgorithmStart>=1.2*MaxDAGTasks: break
            

        while len(Population)<2*popsize:
            if time.time() - AlgorithmStart>=1.2*MaxDAGTasks: break
            a1 = random.randint(0,popsize-1)
            a2 = random.randint(0,popsize-1)
            while a1==a2:
                a2 = random.randint(0,popsize-1)
            Child1,Child2 = crossover_twoPoint(Population[a1],Population[a2])
            Child1,Child2 = mutation(Child1),mutation(Child2)
            Population.append(Child1)
            Population.append(Child2)
            

        non_dominated_sorted_solution = fast_non_dominated_sort(Population)
        CrowdingDistance = crowding_distance(Population,non_dominated_sorted_solution)
        Population = updatePopulation(non_dominated_sorted_solution,CrowdingDistance,Population,popsize)
        non_dominated_sorted_solution = fast_non_dominated_sort(Population)
        CrowdingDistance = crowding_distance(Population,non_dominated_sorted_solution)
        non_dominated_Solution = [Population[i] for i in non_dominated_sorted_solution[0]]

        updatePheromoneMatrices(non_dominated_Solution,VMPheromone,SequencePheromone,SequencePheromone0)
        AlgorithmEnd = time.time() # AlgorithmStart = time.time()
        AlgorithmRunTime = AlgorithmEnd - AlgorithmStart
        if AlgorithmRunTime>=1.2*MaxDAGTasks: break 
    non_dominated_Solution.append(time.time() - AlgorithmStart)  
    # return non_dominated_Solution
    return GlobalResource.RemovePermutation(non_dominated_Solution)






# app = xw.App(visible=True,add_book=False)
# book = app.books.open('.\\ResultExcel\\testszx.xlsx')
# sheet = book.sheets[0]  #引用工作表   os.getcwd()+  # 'Miscellaneous',



listfileName=os.listdir('./data_npy') #     os.getcwd() data_npy
listfileName.sort()
listDeadlineFactor = [0.8,1.1,1.5,1.8]

listWorkflowNum = GlobalResource.listWorkflowNum # .get_globalvalue('listWorkflowNum')   #  [12,155,139,20,82]  #
# TaotalWfNUm = 5 
# listWorkflowNum= random.sample([i for i in range(len(listfileName))],TaotalWfNUm)
for times in range(10):
    for instance in range(len(listWorkflowNum)): # 6,
        print('****************\t\t2019_IJPR_MACO\t Running times=%d \t instance=%d \t\t\t****************'%(times,instance))
        tempmultiWorflow= []
        multiWorflowDeadline = []
        WfDeadline = []
        tempmultiWorflowDAGLevel = []
        MaxDAGTasks = 0
        for n1 in listWorkflowNum[instance][:]:#-3  80, 8,   19-3,
            fileName = listfileName[n1]
            WorkFlowTestName = fileName[0:len(fileName)-12]
            DeadlineFactor = fileName[len(fileName)-7:len(fileName)-4]
            workflow = np.load(os.getcwd()+'/data_npy/'+fileName,allow_pickle=True).item()

            
            DeadlineFactor = workflow.pop('DeadlineFactor')   
            Deadline = workflow.pop('Deadline') # ResetDeadline(workflow,DeadlineFactor)
            '''
            task.MI=1表示具有隐私属性；   task.XFT 为 sub-deadline 
            '''
            DAGLevel = taskTopologicalLevel(workflow)     #DAG分层处理

            getSubDeadline(workflow,Deadline)  # 在此算法中用task.XFT表示Sub-deadline
            WfDeadline.append(Deadline)
            multiWorflowDeadline.append({'Deadline':Deadline,'DeadlineFactor':DeadlineFactor,'WorkflowName':WorkFlowTestName} )
            tempmultiWorflowDAGLevel.append(DAGLevel)
            tempmultiWorflow.append(workflow)
            MaxDAGTasks += len(workflow) # 总任务数  
            del workflow
        ''' 不执行超过1000的'''
        if MaxDAGTasks>=1000:
            continue

        ## 混合云
        PUBLICID  = 0
        PRIVATEID = 1
        HYBRIDCLOUD = [PUBLICID,PRIVATEID]
        DTT = GlobalResource.DTT #传输时间放大倍数
        VMT = [VMType(),PrivateCloudVMType()]

        NumLevellist = [max([len(tempmultiWorflowDAGLevel[i][j]) for j in range(len(tempmultiWorflowDAGLevel[i]))]) for i in range(len(tempmultiWorflowDAGLevel))] 
        EachPBVMTypeNums = math.trunc(np.average(NumLevellist)) #sum(NumLevellist)
        PBVMNums = VMT[PUBLICID].m*EachPBVMTypeNums   #GlobalResource.VMNums
        # VMS =[VMScheduling(VMT.P[i%VMT.m], VMT.N[i%VMT.m]) for i in range(VMNums)]  # len(VMT)

        tempVMS = [[],[]]
        for cloudID in HYBRIDCLOUD:
            if cloudID==PRIVATEID:
                for i in VMT[cloudID].P:
                    for j in range(GlobalResource.NUMofPrivateCloudVM[i]):
                    # if GlobalResource.NUMofPrivateCloudVM[i]>0:
                        tempVMS[cloudID].append(VMScheduling(VMT[cloudID].P[i], VMT[cloudID].N[i]))
            else:
                for i in range(PBVMNums):
                    tempVMS[cloudID].append(VMScheduling(VMT[cloudID].P[i%VMT[cloudID].m], VMT[cloudID].N[i%VMT[cloudID].m]))
        PRVMNums = len(tempVMS[PRIVATEID])


        NonDominSalps = MACO()
        str1 = str(instance)+'_'+str(len(listWorkflowNum[instance]))+'_'+str(MaxDAGTasks)+'_'+str(times) # -'+str1+'
        np.save(os.getcwd()+'/ParetoFront/'+'2019_IJPR_MACO_NF-'+str1+'.npy', NonDominSalps)
        print('****************\t\t\t2019_IJPR_MACO\t End times=%d \t instance=%d \t\t****************'%(times,instance))

