'''[1] H. Hafsi, H. Gharsellaoui, and S. Bouamama, “Genetically-modified Multi-objective Particle Swarm Optimization approach for high-performance computing workflow scheduling,” Appl. Soft Comput., vol. 122, p. 108791, 2022, doi: 10.1016/j.asoc.2022.108791.'''
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
# import xlwings as xw
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
  
    plt.rcParams["font.family"] = "times new roman"
    colorNum = 10
    cmap = plt.get_cmap('gist_rainbow',colorNum) #  spring  Paired autumn
    colors = cmap(np.linspace(0,1,colorNum))
    # ['red', 'royalblue', 'gold', 'lawngreen', 'orange', 'blueviolet']
    # colors = ['dimgray','tan','lightblue','coral','g','r','silver','y','c']'lightseagreen',
    marks = ["","\\","/","X","+",".","*","o"]
    plt.figure(dpi=85)
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

        crowding_distance.append(distance)
    return crowding_distance

def updatePopulation_Leaders(front,distance,Population,popsize,LeaderSize):
    for level in range(len(front)):
        temp = []
        for i in range(len(front[level])):
            temp.append([front[level][i],distance[level][i]])            
        temp = sorted(temp, key=lambda temp: temp[1])
        front[level] = [temp[i][0] for i in range(len(temp))]
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

    Leaders = [] 
    objList = []
    kk = 0
    for level in range(len(front)):
        for i in range(len(front[level])):  
            if (len(Leaders)>0):
                if [Population[front[level][i]].objectives.Cost,Population[front[level][i]].objectives.Energy,Population[front[level][i]].objectives.TotalTardiness] not in objList:
                # if ((Leaders[len(Leaders)-1].objectives.Cost!=Population[front[level][i]].objectives.Cost)and
                    # (Leaders[len(Leaders)-1].objectives.Energy!=Population[front[level][i]].objectives.Energy)):                  
                    Leaders.append(Population[front[level][i]])
                    objList.append([Leaders[len(Leaders)-1].objectives.Cost,Leaders[len(Leaders)-1].objectives.Energy,Leaders[len(Leaders)-1].objectives.TotalTardiness]) 
                    kk += 1
            else:
                Leaders.append(Population[front[level][i]]) 
                objList.append([Leaders[len(Leaders)-1].objectives.Cost,Leaders[len(Leaders)-1].objectives.Energy,Leaders[len(Leaders)-1].objectives.TotalTardiness])
                kk += 1
            if kk== LeaderSize: break
        if kk== LeaderSize: break
    LocalBest = []
    objList = []
    for i in range(min(len(front[0]),popsize)):
        if (len(LocalBest)>0):
            if [Population[front[0][i]].objectives.Cost,Population[front[0][i]].objectives.Energy,Population[front[0][i]].objectives.TotalTardiness] not in objList:
            # if ((LocalBest[len(LocalBest)-1].objectives.Cost!=Population[front[0][i]].objectives.Cost)and
            #     (LocalBest[len(LocalBest)-1].objectives.Energy!=Population[front[0][i]].objectives.Energy)):
                LocalBest.append(Population[front[0][i]])
                objList.append([LocalBest[len(LocalBest)-1].objectives.Cost,LocalBest[len(LocalBest)-1].objectives.Energy,LocalBest[len(LocalBest)-1].objectives.TotalTardiness])
        else:         
            LocalBest.append(Population[front[0][i]]) 
            objList.append([LocalBest[len(LocalBest)-1].objectives.Cost,LocalBest[len(LocalBest)-1].objectives.Energy,LocalBest[len(LocalBest)-1].objectives.TotalTardiness])    
    return newPopulation,Leaders,LocalBest



def updateChromosome(chromosome):
    for k in  range(len(TaskList)):
        i = TaskList[k][0]
        j = TaskList[k][1]
        if ((chromosome.VMOrder[k]>=TotalVMs)or(chromosome.VMOrder[k]<0)
                    or((chromosome.multiworflow[i][j].MI==PRIVATEID)
                    and(chromosome.VMList[chromosome.VMOrder[k]][0]!=PRIVATEID))):
            if chromosome.multiworflow[i][j].MI==PRIVATEID:
                CloudID = PRIVATEID
                # r1 = sum(GlobalResource.NUMofPrivateCloudVM)
                VmID = random.randint(0,PRVMs-1)
            else:
                CloudID = random.choice(HYBRIDCLOUD)
                if CloudID ==PRIVATEID:## yes
                    # r1 = sum(GlobalResource.NUMofPrivateCloudVM)
                    VmID = random.randint(0,PRVMs-1)
                else:  ##  yes
                    # r1 = sum(chromosome.cloneVector)
                    VmID = random.randint(0,PBVMs-1)
            chromosome.multiworflow[i][j].VMnum = [CloudID,VmID]
            chromosome.VMOrder[k] = chromosome.VMList.index([CloudID,VmID])
        else:
            chromosome.multiworflow[i][j].VMnum = chromosome.VMList[chromosome.VMOrder[k]]

    chromosome.scheduleMatrix = np.full((MaxDAGTasks,TotalVMs),0,dtype=np.int16)  # np.zeros((MaxDAGTasks,MaxDAGTasks)) # len(TaskList),sum(GlobalResource.NUMofPrivateCloudVM)+sum(chromosome.cloneVector)
    for i in chromosome.TasksOrder:
        chromosome.scheduleMatrix[TaskList.index(i),chromosome.VMOrder[TaskList.index(i)]] = chromosome.TasksOrder.index(i)+1

    CalcaulateTaskObject_MultiWorkflow(chromosome)
    return chromosome

def crossoverParticles(salpA,salpB):
    global  TaskList # VMList, OriginalMWOrder

    def FirstEqual(salpA,salpB,pos):
        list1 = [TaskList.index(salpA.TasksOrder[i] ) for i in range(pos)  ]
        list2 = [TaskList.index(salpB.TasksOrder[i] ) for i in range(pos)  ]
        Eq = pos
        while set(list1)!=set(list2):  # list1.sort()==list2.sort():    # 
            Eq += 1
            list1 = [TaskList.index(salpA.TasksOrder[i] ) for i in range(Eq)  ]
            list2 = [TaskList.index(salpB.TasksOrder[i] ) for i in range(Eq)  ]
        return Eq

    def SwapTask(salpA,salpB,start,end):
        NewsalpA = copy.deepcopy(salpA)
        NewsalpB = copy.deepcopy(salpB)
        for i in range(start,end+1):
            LA = NewsalpA.scheduleMatrix[i,:].copy()
            LB = NewsalpB.scheduleMatrix[i,:].copy()
            NewsalpA.scheduleMatrix[i,:] = LB
            NewsalpB.scheduleMatrix[i,:] = LA
            # NewsalpA.scheduleMatrix[i,:], NewsalpB.scheduleMatrix[i,:] = NewsalpB.scheduleMatrix[i,:], NewsalpA.scheduleMatrix[i,:]


        NewsalpA.scheduleMatrix[[start,end],:], NewsalpB.scheduleMatrix[[start,end],:] = NewsalpB.scheduleMatrix[[start,end],:], NewsalpA.scheduleMatrix[[start,end],:]
        for i in range(start,end+1):
            NewsalpA.TasksOrder[i] = salpB.TasksOrder[i]   # TaskList[i]
            NewsalpA.VMOrder[i] = salpB.VMOrder[i]
            NewsalpA.multiworflow[NewsalpA.TasksOrder[i][0]][NewsalpA.TasksOrder[i][1]].VMnum = NewsalpA.VMList[NewsalpA.VMOrder[i]]

            NewsalpB.TasksOrder[i] = salpA.TasksOrder[i]   # TaskList[i]
            NewsalpB.VMOrder[i] = salpA.VMOrder[i]
            NewsalpB.multiworflow[NewsalpB.TasksOrder[i][0]][NewsalpB.TasksOrder[i][1]].VMnum = NewsalpB.VMList[NewsalpB.VMOrder[i]]        
        return NewsalpA,NewsalpB

    pos = random.randint(1,int(MaxDAGTasks/4))
    start = FirstEqual(salpA,salpB,pos)+1
    kk = 0
    while start>=MaxDAGTasks:
        pos = random.randint(1,int(MaxDAGTasks/10))
        start = FirstEqual(salpA,salpB,pos)+1
        kk += 1
        if kk>9: break
    if start>=MaxDAGTasks:
        return salpA,salpB
    
    pos = random.randint(start,MaxDAGTasks)
    end = FirstEqual(salpA,salpB,pos)-1
    start -= 1
    if start==end:
        return salpA,salpB
    NewsalpA,NewsalpB = SwapTask(salpA,salpB,start,end)
    # CalcaulateTaskObject_MultiWorkflow(NewsalpA)
    # CalcaulateTaskObject_MultiWorkflow(NewsalpB)
    return NewsalpA,NewsalpB
    
def Mutate(Child):
    def Order_Mutation(Child):
        pos = random.randint(0,MaxDAGTasks-1)
        task = Child.TasksOrder[pos]
        minPos = MaxDAGTasks-1
        for c in Child.multiworflow[task[0]][task[1]].outputs:
            minPos = min(minPos, Child.TasksOrder.index([task[0],c.id]))

        task = Child.TasksOrder.pop(pos)
        Child.TasksOrder.insert(minPos-1,task)
        for k in range(pos,minPos):
            i = Child.TasksOrder[k]
            Child.scheduleMatrix[TaskList.index(i),Child.VMOrder[TaskList.index(i)]] = k+1   # Child.TasksOrder.index(i)
        # CalcaulateTaskObject_MultiWorkflow(Child)
        return Child
    def VM_Mutation(Child):
        pos1 = random.randint(0,TotalVMs-1)
        pos2 = random.randint(0,TotalVMs-1)
        while pos1==pos2:
            pos2 = random.randint(0,TotalVMs-1)
        if pos1>pos2:
            pos1,pos2 = pos2,pos1
        Child.scheduleMatrix[:,[pos1,pos2]] = Child.scheduleMatrix[:,[pos2,pos1]]

        
        # s1 = sorted(Child.VMOrder)
        for i in [pos1,pos2]:
            for j in range(MaxDAGTasks):
                if Child.scheduleMatrix[j,i]>0:
                    Child.VMOrder[j] = i # int(Child.scheduleMatrix[j,i]) # NewsalpB.VMList[NewsalpB.VMOrder[i]]
                    Child.multiworflow[TaskList[j][0]][TaskList[j][1]].VMnum = Child.VMList[Child.VMOrder[j]]
                    if (Child.multiworflow[TaskList[j][0]][TaskList[j][1]].MI==PRIVATEID 
                                        and(Child.VMList[Child.VMOrder[j]][0]!=PRIVATEID)):
                        CloudID = PRIVATEID
                        # r1 = sum(GlobalResource.NUMofPrivateCloudVM)
                        VmID = random.randint(0,PRVMs-1)
                        Child.multiworflow[TaskList[j][0]][TaskList[j][1]].VMnum = [CloudID,VmID]
                        Child.VMOrder[j] = Child.VMList.index([CloudID,VmID])
                        Child.scheduleMatrix[j,i], Child.scheduleMatrix[j,Child.VMOrder[j]] = Child.scheduleMatrix[j,Child.VMOrder[j]],Child.scheduleMatrix[j,i]
        CalcaulateTaskObject_MultiWorkflow(Child)
        return Child
    def CV_Mutation(Child):
        pos1 = random.randint(0,VMT[PUBLICID].m-1)
        pos2 = random.randint(0,VMT[PUBLICID].m-1)
        while pos1==pos2:
            pos2 = random.randint(0,VMT[PUBLICID].m-1)
        if pos1>pos2:
            pos1,pos2 = pos2,pos1
        Child.cloneVector[pos1],Child.cloneVector[pos2] = Child.cloneVector[pos2], Child.cloneVector[pos1]
        Child.PBVMIndexlist = []
        for i in range(VMT[PUBLICID].m):
            for j in range(Child.cloneVector[i]):
                Child.PBVMIndexlist.append(i)

        Child.VMList = []
        for cloudID in HYBRIDCLOUD:
            kk = 0
            if cloudID==PRIVATEID:
                for i in VMT[cloudID].P:
                    for j in range(GlobalResource.NUMofPrivateCloudVM[i]):
                        Child.VMList.append([cloudID,kk])
                        kk += 1                    
            else:
                for i in Child.PBVMIndexlist: 
                    Child.VMList.append([cloudID,kk])
                    kk += 1
        for i in  range(len(TaskList)):
            dag = TaskList[i][0]
            taskid = TaskList[i][1]
            Child.multiworflow[dag][taskid].VMnum = Child.VMList[Child.VMOrder[i]]
        CalcaulateTaskObject_MultiWorkflow(Child)
        return Child
    i = random.randint(1,3) # 3 # 
    if i == 1:
        return Order_Mutation(Child)
    elif i == 2:
        return VM_Mutation(Child)
    else:
        return CV_Mutation(Child)


###########################################################
###########################################################

def ChromosomeInitialization():
    # global PUBLICID,PRIVATEID,multiWorflow,VMS,multiWorflowDAGLevel,LevelMaxFinishTtime,FT_Star,ListLevelVM  # 
    chromosome = ChromClass()
    chromosome.multiworflow = copy.deepcopy(tempmultiWorflow)
    multiWorflowDAGLevel = copy.deepcopy(tempmultiWorflowDAGLevel)
    
    chromosome.TasksOrder = []
    TotalLevel = sum([len(multiWorflowDAGLevel[i]) for i in range(len(multiWorflowDAGLevel))])
    ScheduledMultiWFLevel = [0 for i in range(len(chromosome.multiworflow))] # 每个工作流已调度的层数
    for kk in range(TotalLevel):
        workflowNum = random.randint(0,len(chromosome.multiworflow)-1)
        while ScheduledMultiWFLevel[workflowNum]==len(multiWorflowDAGLevel[workflowNum]):
            workflowNum = random.randint(0,len(chromosome.multiworflow)-1)
        random.shuffle(multiWorflowDAGLevel[workflowNum][ScheduledMultiWFLevel[workflowNum]])
        chromosome.TasksOrder= chromosome.TasksOrder + [[workflowNum,i] for i in multiWorflowDAGLevel[workflowNum][ScheduledMultiWFLevel[workflowNum]]]
        ScheduledMultiWFLevel[workflowNum] += 1

    # chromosome.cloneVector = [random.randint(0,EachPBVMTypeNums-1) for i in range(VMT[PUBLICID].m)]
    # MaxDAGTasks
    a_list = [random.randint(0,PBVMs) for i in range(VMT[PUBLICID].m-1)] # random.sample(range(1,10),10-1)
    a_list.append(0)
    a_list.append(PBVMs)
    a_list.sort()
    chromosome.cloneVector = [a_list[i+1]-a_list[i] for i in range(VMT[PUBLICID].m)]

    chromosome.PBVMIndexlist = []
    for i in range(VMT[PUBLICID].m):
        for j in range(chromosome.cloneVector[i]):
            chromosome.PBVMIndexlist.append(i)

    chromosome.VMList = []
    for cloudID in HYBRIDCLOUD:
        kk = 0
        if cloudID==PRIVATEID:
            for i in VMT[cloudID].P:
                for j in range(GlobalResource.NUMofPrivateCloudVM[i]):
                    chromosome.VMList.append([cloudID,kk])
                    kk += 1                    
        else:
            for i in chromosome.PBVMIndexlist: 
                chromosome.VMList.append([cloudID,kk])
                kk += 1

    # random.shuffle(SalpPopulation[g].LevelTask[i][j]) # 随机顺序
    for i in range(len(chromosome.multiworflow)):
        for j in range(len(chromosome.multiworflow[i])):
            if chromosome.multiworflow[i][j].MI==PRIVATEID: ## yes
                CloudID = PRIVATEID
                # r1 = sum(GlobalResource.NUMofPrivateCloudVM)
                VmID = random.randint(0,PRVMs-1)
            else:
                CloudID = random.choice(HYBRIDCLOUD)
                if CloudID ==PRIVATEID:## yes
                    # r1 = sum(GlobalResource.NUMofPrivateCloudVM)
                    VmID = random.randint(0,PRVMs-1)
                else:  ##  yes
                    # r1 = sum(chromosome.cloneVector)
                    VmID = random.randint(0,PBVMs-1)
            chromosome.multiworflow[i][j].VMnum = [CloudID,VmID]
    chromosome.VMOrder = []
    for i in  range(len(TaskList)):
        dag = TaskList[i][0]
        taskid = TaskList[i][1]
        chromosome.VMOrder.append(chromosome.VMList.index(chromosome.multiworflow[dag][taskid].VMnum))

    # chromosome.scheduleMatrix = np.full((MaxDAGTasks,MaxDAGTasks),0,dtype=np.int16)  # np.zeros((MaxDAGTasks,MaxDAGTasks)) # len(TaskList),sum(GlobalResource.NUMofPrivateCloudVM)+sum(chromosome.cloneVector)
    chromosome.scheduleMatrix = np.full((MaxDAGTasks,TotalVMs),0,dtype=np.int16)  # 
    for i in chromosome.TasksOrder:
        chromosome.scheduleMatrix[TaskList.index(i),chromosome.VMOrder[TaskList.index(i)]] = chromosome.TasksOrder.index(i)+1

    CalcaulateTaskObject_MultiWorkflow(chromosome)
    return chromosome

def CalcaulateTaskObject_MultiWorkflow(chromosome):
    chromosome.VMSchedule = [[],[]]
    for cloudID in HYBRIDCLOUD:
        if cloudID==PRIVATEID:
            for i in VMT[cloudID].P:
                for j in range(GlobalResource.NUMofPrivateCloudVM[i]):
                    chromosome.VMSchedule[cloudID].append(VMScheduling(VMT[cloudID].P[i], VMT[cloudID].N[i]))
        else:
            for i in chromosome.PBVMIndexlist:
                chromosome.VMSchedule[cloudID].append(VMScheduling(VMT[cloudID].P[i], VMT[cloudID].N[i]))

    # chromosome.VMSchedule = copy.deepcopy(tempVMS)
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

class ChromClass:
    def __init__(self):
        self.VMOrder=None
        self.TasksOrder=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.scheduleMatrix=None
        self.cloneVector=None
        self.PBVMIndexlist = None
        self.VMList = None
        # self.pm = None
        # self.pc = None


def GMPSO(): 
    global  TaskList # VMList, OriginalMWOrder
    popsize = 100    
    max_iter = 300
    LeadersSize = 50
    CrosPro = 0.5
    MutaPro = 0.5
    GMJump = 3
    GMParents = 50
    W = 0.1
    c1 = 2 # 1.5 + random.random()
    c2 = 2 # 1.5 + random.random()
    AlgorithmStart = time.time()
    TaskList = []
    for dag in range(len(tempmultiWorflow)):
        for taskid in range(len(tempmultiWorflow[dag])):
            TaskList.append([dag,taskid])

    # VMList = []
    # for cloudid in range(len(tempVMS)):
    #     for VMid in range(len(tempVMS[cloudid])):
    #         VMList.append([cloudid,VMid])

    Population = [ChromosomeInitialization() for g in range(popsize)]
    non_dominated_sorted_solution = fast_non_dominated_sort(Population)
    CrowdingDistance = crowding_distance(Population,non_dominated_sorted_solution) 
    Population,Leaders,LocalBest = updatePopulation_Leaders(non_dominated_sorted_solution,CrowdingDistance,Population,popsize,LeadersSize) 
    # Leaders,LocalBest = SelectLeaders(non_dominated_sorted_solution,CrowdingDistance,Population,LeadersSize)
    vel=np.zeros((popsize,MaxDAGTasks))
    for iter in range(max_iter):        
        for i in range(popsize):
            gb0 = random.randint(0,len(Leaders)-1)
            pb0 = random.randint(0,len(LocalBest)-1)
            gBest = Leaders[gb0]
            pBest = LocalBest[pb0]
            # Population[i].VMOrder[j]
            for j in range (MaxDAGTasks):
                r1 = random.random()
                r2 = random.random()
                vel[i,j] = W*vel[i,j]+c1*r1*(pBest.VMOrder[j]-Population[i].VMOrder[j])+c2*r2*(gBest.VMOrder[j]-Population[i].VMOrder[j]) 
                Population[i].VMOrder[j] = Population[i].VMOrder[j]+int(vel[i,j])
            Population[i] = updateChromosome(Population[i])
            if time.time() - AlgorithmStart>=1.2*MaxDAGTasks: break
        Offsprings = []
        if iter%GMJump==0:  #  True: # 
            for i in range(GMParents):
                a1 = random.randint(0,popsize-1)
                a2 = random.randint(0,len(Leaders)-1)
                # Population[a1],Leaders[a2]
                Child1 = copy.deepcopy(Population[a1])
                Child2 = copy.deepcopy(Leaders[a2])
                if random.random()<0.5:
                    Child1,Child2 = crossoverParticles(Child1,Child2)  
                if random.random()<0.5:     
                    Child1 = Mutate(Child1)
                if random.random()<0.5:
                    Child2 = Mutate(Child2)
                CalcaulateTaskObject_MultiWorkflow(Child1)
                CalcaulateTaskObject_MultiWorkflow(Child2)
                Offsprings.append(Child1) 
                Offsprings.append(Child2)
                if time.time() - AlgorithmStart>=1.2*MaxDAGTasks: break
        for i in range(popsize):
            if random.random()<0.5:
                Population[i] = Mutate(Population[i])
                CalcaulateTaskObject_MultiWorkflow(Population[i])
            if time.time() - AlgorithmStart>=1.2*MaxDAGTasks: break
        Population = Population + Leaders + LocalBest + Offsprings
        non_dominated_sorted_solution = fast_non_dominated_sort(Population)
        CrowdingDistance = crowding_distance(Population,non_dominated_sorted_solution) 
        Population,Leaders,LocalBest = updatePopulation_Leaders(non_dominated_sorted_solution,CrowdingDistance,Population,popsize,LeadersSize) 
        AlgorithmEnd = time.time() # AlgorithmStart = time.time()
        AlgorithmRunTime = AlgorithmEnd - AlgorithmStart
        if AlgorithmRunTime>=1.2*MaxDAGTasks: break    
    Leaders.append(time.time() - AlgorithmStart )
    # return Leaders
    return GlobalResource.RemovePermutation(Leaders)    

# app = xw.App(visible=True,add_book=False)
# book = app.books.open('.\\ResultExcel\\testszx.xlsx')
# sheet = book.sheets[0]  #引用工作表   os.getcwd()+  # 'Miscellaneous',

listfileName=os.listdir('./data_npy') #     os.getcwd() data_npy
listfileName.sort()
listDeadlineFactor = [0.8,1.1,1.5,1.8]

listWorkflowNum = GlobalResource.listWorkflowNum # .get_globalvalue('listWorkflowNum')   #  [12,155,139,20,82]  #
# TaotalWfNUm = 5 
# listWorkflowNum= random.sample([i for i in range(len(listfileName))],TaotalWfNUm)
repeattimes = 1  #10   # The repeat times is 10 in my paper
totalNumbersTestProblems = 1 # len(listWorkflowNum)  # The total numbers of test problems is len(listWorkflowNum).
for times in range(repeattimes):  
    for instance in range(totalNumbersTestProblems):
        print('****************\t\t2022_ASC_GMPSO\t Running times=%d \t instance=%d \t\t\t****************'%(times,instance))
        tempmultiWorflow= []
        multiWorflowDeadline = []
        WfDeadline = []
        tempmultiWorflowDAGLevel = []
        MaxDAGTasks= 0
        for n1 in listWorkflowNum[instance][:]:#-3  80, 8,   19-3,
            fileName = listfileName[n1]
            WorkFlowTestName = fileName[0:len(fileName)-12]
            DeadlineFactor = fileName[len(fileName)-7:len(fileName)-4]
            workflow = np.load(os.getcwd()+'/data_npy/'+fileName,allow_pickle=True).item()

            
            DeadlineFactor = workflow.pop('DeadlineFactor')   
            Deadline = workflow.pop('Deadline') # ResetDeadline(workflow,DeadlineFactor)

            DAGLevel = taskTopologicalLevel(workflow)    

            getSubDeadline(workflow,Deadline) 
            WfDeadline.append(Deadline)
            multiWorflowDeadline.append({'Deadline':Deadline,'DeadlineFactor':DeadlineFactor,'WorkflowName':WorkFlowTestName} )
            tempmultiWorflowDAGLevel.append(DAGLevel)
            tempmultiWorflow.append(workflow)
            # MaxDAGTasks = max(len(workflow),MaxDAGTasks) # 选择DAG 最多的任务数
            MaxDAGTasks += len(workflow) # 总任务数  
            del workflow



        ## 
        PUBLICID  = 0
        PRIVATEID = 1
        HYBRIDCLOUD = [PUBLICID,PRIVATEID]
        DTT = GlobalResource.DTT 
        VMT = [VMType(),PrivateCloudVMType()]
        PRVMs = sum(GlobalResource.NUMofPrivateCloudVM)
        # PBVMs = MaxDAGTasks - PRVMs
        NumLevellist = [max([len(tempmultiWorflowDAGLevel[i][j]) for j in range(len(tempmultiWorflowDAGLevel[i]))]) for i in range(len(tempmultiWorflowDAGLevel))] 
        EachPBVMTypeNums = math.trunc(np.average(NumLevellist)) #sum(NumLevellist)
        PBVMs = VMT[PUBLICID].m*EachPBVMTypeNums   #GlobalResource.VMNums
        # VMS =[VMScheduling(VMT.P[i%VMT.m], VMT.N[i%VMT.m]) for i in range(VMNums)]  # len(VMT)        
        TotalVMs = PBVMs + PRVMs
        NonDominSalps = GMPSO()
        str1 = str(instance)+'_'+str(len(listWorkflowNum[instance]))+'_'+str(MaxDAGTasks)+'_'+str(times) # -'+str1+'
        np.save(os.getcwd()+'/GMPSO/'+'2022_ASC_GMPSO_NF-'+str1+'.npy', NonDominSalps)
        print('****************\t\t\t2022_ASC_GMPSO\t Running times=%d \t instance=%d \t\t****************'%(times,instance))

