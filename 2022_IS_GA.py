'''[1] X. Xia, H. Qiu, X. Xu, and Y. Zhang, “Multi-objective workflow scheduling based on genetic algorithm in cloud environment,” Inf. Sci. (Ny)., vol. 606, pp. 38–59, 2022, doi: 10.1016/j.ins.2022.05.053.'''
from cmath import inf
import os
from sys import get_asyncgen_hooks
from matplotlib import markers 
from numpy.lib.function_base import append, copy
from requests import delete
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

    # ## 按执行时间升序排列
    # for k in range(len(DAGLevel)):
    #     for i in range(len(DAGLevel[k])-1):
    #         for j in range(i+1,len(DAGLevel[k])):
    #             if self[DAGLevel[k][i]].runtime<self[DAGLevel[k][j]].runtime:
    #                 DAGLevel[k][i],DAGLevel[k][j] = DAGLevel[k][j], DAGLevel[k][i]
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

# def DetermineWhether2Dominate(salpA,salpB): ## Cost   Energy
#     ''' salpA 可支配 salpB  '''
#     if ((salpA.objectives.Cost<=salpB.objectives.Cost) and(salpA.objectives.Energy<=salpB.objectives.Energy)):
#         # return True  # 包含相等的
#         if ((salpA.objectives.Cost<salpB.objectives.Cost) or (salpA.objectives.Energy<salpB.objectives.Energy)):
#             return True
#     return False

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
        
    ##  以下是根据经典的拥挤距离更新非劣解集
    # NonDominSalps = CalcuCrowdDistance_UpdateNon_domin(NonDominSalps,NumNonDominated)
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
        ranks.append(0)
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

   

#######################################################
#######################################################
#######################################################

def getLCS(s1, s2):
    '''最长公共子序列 https://blog.csdn.net/weixin_42018258/article/details/80670067'''
    size1 = len(s1) + 1
    size2 = len(s2) + 1
    chess = [[["", 0] for j in list(range(size2))] for i in list(range(size1))]
    for i in list(range(1, size1)):
        chess[i][0][0] = s1[i - 1]
    for j in list(range(1, size2)):
        chess[0][j][0] = s2[j - 1]
    for i in list(range(1, size1)):
        for j in list(range(1, size2)):
            if s1[i - 1] == s2[j - 1]:
                chess[i][j] = ['↖', chess[i - 1][j - 1][1] + 1]
            elif chess[i][j - 1][1] > chess[i - 1][j][1]:
                chess[i][j] = ['←', chess[i][j - 1][1]]
            else:
                chess[i][j] = ['↑', chess[i - 1][j][1]]
    i = size1 - 1
    j = size2 - 1
    s3 = []
    while i > 0 and j > 0:
        if chess[i][j][0] == '↖':
            s3.append(chess[i][0][0])
            i -= 1
            j -= 1
        if chess[i][j][0] == '←':
            j -= 1
        if chess[i][j][0] == '↑':
            i -= 1
    s3.reverse()
    return s3

def ChromosomeInitialization():
    '''初始化'''
    # global PUBLICID,PRIVATEID,multiWorflow,VMS,multiWorflowDAGLevel,LevelMaxFinishTtime,FT_Star,ListLevelVM  # 
    chromosome = ChromClass()
    chromosome.multiworflow = copy.deepcopy(tempmultiWorflow)
    DAG = copy.deepcopy(tempmultiWorflow)
    T= []
    for each in range(len(DAG)):        
        list1 = [taskId for taskId,task in DAG[each].items()]
        DAG[each][len(DAG[each])] = Task(len(DAG[each]),name = 'entry')
        T.append([each,len(DAG[each])-1])
        for taskId in list1:
            T.append([each,taskId])
            if DAG[each][taskId].inputs == []:   #原源节点 size = 0  JITCAWorkflow[len(JITCAWorkflow)-1]
                tout = File('EntryOut', id = len(DAG[each])-1)
                DAG[each][taskId].inputs.append(tout)
                tout = File('Entry', id = taskId)
                DAG[each][len(DAG[each])-1].addOutput(tout)
    WFnum = random.randint(0,len(DAG)-1)
    TNum = DAG[WFnum][len(DAG[WFnum])-1].id

    chromosome.Y = [[WFnum,TNum]]
    T.remove([WFnum,TNum])
    S = []
    while T!=[]:
        for ti in T:            
            nofind = True
            for eachPar in DAG[ti[0]][ti[1]].inputs:
                if [ti[0],eachPar.id] not in chromosome.Y:
                    nofind = False
                    break
            if nofind:
                S.append(ti)
        randomTask = S[random.randint(0,len(S)-1)]
        T.remove(randomTask)
        chromosome.Y.append(randomTask)
        S = []
    for WFnum in range(len(DAG)): 
        chromosome.Y.remove([WFnum,len(DAG[WFnum])-1])
    del DAG

    for i in range(len(chromosome.multiworflow)):
        AvgTime = 0
        for j in range(len(chromosome.multiworflow[i])):
            AvgTime += chromosome.multiworflow[i][j].runtime
        AvgTime = AvgTime/len(chromosome.multiworflow[i])
        for j in range(len(chromosome.multiworflow[i])):
            if chromosome.multiworflow[i][j].runtime>AvgTime:
                if chromosome.multiworflow[i][j].MI==PRIVATEID: ## yes
                    CloudID = PRIVATEID
                    r1 = random.randint(0,GlobalResource.NUMofPrivateCloudVM[-1]-1)
                    VmID = sum(GlobalResource.NUMofPrivateCloudVM)-1 - r1
                else:
                    CloudID = random.choice(HYBRIDCLOUD)
                    if CloudID ==PRIVATEID: ## yes
                        r1 = random.randint(0,GlobalResource.NUMofPrivateCloudVM[-1]-1)
                        VmID = sum(GlobalResource.NUMofPrivateCloudVM)-1 - r1
                    else: ## yes
                        r1 = random.randint(0,EachPBVMTypeNums-1)
                        VmID = EachPBVMTypeNums*(VMT[CloudID].m-1) + r1
            else:
                if chromosome.multiworflow[i][j].MI==PRIVATEID: ## yes
                    CloudID = PRIVATEID
                    r1 = sum(GlobalResource.NUMofPrivateCloudVM[0:-1])-1
                    VmID = random.randint(0,r1)
                else:
                    CloudID = random.choice(HYBRIDCLOUD)
                    if CloudID ==PRIVATEID:## yes
                        r1 = sum(GlobalResource.NUMofPrivateCloudVM[0:-1])-1
                        VmID = random.randint(0,r1)
                    else:  ##  yes
                        Vmtype = random.randint(0,VMT[CloudID].m-2)
                        nums = random.randint(0,EachPBVMTypeNums-1)
                        VmID =  EachPBVMTypeNums*Vmtype + nums  # random.randint(0,PBVMNums-1)
            chromosome.multiworflow[i][j].VMnum = [CloudID,VmID]
    chromosome.X = []
    for y1 in chromosome.Y:
        chromosome.X.append(chromosome.multiworflow[y1[0]][y1[1]].VMnum  )
    chromosome.pm = 1/max( [len(chromosome.multiworflow[i]) for i in range(len(chromosome.multiworflow))])
    chromosome.pc = 1

    CalcaulateTaskObject_MultiWorkflow(chromosome)
    return chromosome

def CalcaulateTaskObject_MultiWorkflow(chromosome):
    chromosome.VMSchedule = copy.deepcopy(tempVMS)
    for i in chromosome.Y:
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
        self.X=None
        self.Y=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.pm = None
        self.pc = None

# def DetermineWhether2Dominate(salpA,salpB): ## Cost   Energy
#     ''' salpA 可支配 salpB  '''
#     if ((salpA.objectives.Cost<=salpB.objectives.Cost) and(salpA.objectives.Energy<=salpB.objectives.Energy)):
#         # return True  # 包含相等的
#         if ((salpA.objectives.Cost<salpB.objectives.Cost) or (salpA.objectives.Energy<salpB.objectives.Energy)):
#             return True
#     return False


def fast_non_dominated_sort(Population):
    Population.sort(key=operator.attrgetter('objectives.Energy','objectives.Cost'))
    kk= 0
    while True:
        i = kk +1
        # if ((Population[i].objectives.Cost==Population[kk].objectives.Cost) and(Population[i].objectives.Energy==Population[kk].objectives.Energy)):
        if GlobalResource.DetermineWhether2Equal(Population[i],Population[kk]):
            Population.pop(i)
        else:
            kk += 1
        if kk>=len(Population)-1:
            break


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

def crossover(salpA,salpB):    
    NewsalpA = copy.deepcopy(salpA)
    NewsalpB = copy.deepcopy(salpB)

    position = random.randint(1,len(salpA.X)-1-1)
    set1 = [ NewsalpA.Y[i] for i in range(position)]
    kk = position
    for i in salpB.Y:
        if i not in set1:
            NewsalpA.Y[kk] = i
            kk += 1            
    set1 = [ NewsalpB.Y[i] for i in range(position)]
    kk = position
    for i in salpA.Y:
        if i not in set1:
            NewsalpB.Y[kk] = i
            kk += 1

    position = random.randint(1,len(salpA.X)-1-1)
    for i in range(position,len(salpA.X)):
        NewsalpA.X[i] = salpB.X[i]
    for i in range(position,len(salpA.X)):
        NewsalpB.X[i] = salpA.X[i]
    for i in range(len(salpA.X)):  ##  修订交叉结果，具有隐私属性的任务必须在私有云
        task = NewsalpA.Y[i]
        if (NewsalpA.multiworflow[task[0]][task[1]].MI==PRIVATEID and (NewsalpA.X[i][0]!=PRIVATEID)):
            CloudID = PRIVATEID
            r1 = sum(GlobalResource.NUMofPrivateCloudVM)-1
            VmID = random.randint(0,r1)
            NewsalpA.multiworflow[task[0]][task[1]].VMnum = [CloudID,VmID]
            NewsalpA.X[i] = [CloudID,VmID] 
        task = NewsalpB.Y[i]
        if (NewsalpB.multiworflow[task[0]][task[1]].MI==PRIVATEID and (NewsalpB.X[i][0]!=PRIVATEID)):
            CloudID = PRIVATEID
            r1 = sum(GlobalResource.NUMofPrivateCloudVM)-1
            VmID = random.randint(0,r1)
            NewsalpB.multiworflow[task[0]][task[1]].VMnum = [CloudID,VmID]
            NewsalpB.X[i] = [CloudID,VmID]

    NewsalpA.multiworflow = copy.deepcopy(tempmultiWorflow)
    NewsalpB.multiworflow = copy.deepcopy(tempmultiWorflow)
    for i in range(len(salpA.X)):
        y1 = NewsalpA.Y[i] 
        NewsalpA.multiworflow[y1[0]][y1[1]].VMnum = NewsalpA.X[i]
        y1 = NewsalpB.Y[i] 
        NewsalpB.multiworflow[y1[0]][y1[1]].VMnum = NewsalpB.X[i]
    CalcaulateTaskObject_MultiWorkflow(NewsalpA)
    CalcaulateTaskObject_MultiWorkflow(NewsalpB)
    del salpA,salpB
    return NewsalpA,NewsalpB

def mutation(salpA):  # ,salpB
    # NewsalpA = copy.deepcopy(salpA)
    # NewsalpB = copy.deepcopy(salpB)
    while True:
        position = random.randint(0,len(salpA.X)-1)
        task = salpA.Y.pop(position)
        # 父节点任务大的索引
        minMAXIndex = 0
        for parentNode in salpA.multiworflow[task[0]][task[1]].inputs:
            P = [task[0],parentNode.id]
            minMAXIndex = max(minMAXIndex,salpA.Y.index(P))
        # 子节点任务最小的索引
        maxMinIndex = len(salpA.X)
        for parentNode in salpA.multiworflow[task[0]][task[1]].outputs:
            P = [task[0],parentNode.id]
            maxMinIndex = min(maxMinIndex,salpA.Y.index(P))  
        if minMAXIndex<maxMinIndex:
            InsertPosition = random.randint(minMAXIndex+1,maxMinIndex)
            salpA.Y.insert(InsertPosition,task)
            break
        else:
            salpA.Y.insert(minMAXIndex,task)

    # position = random.randint(0,len(salpA.X)-1)
    # task = salpB.Y.pop(position)
    # # 父节点任务大的索引
    # minMAXIndex = 0
    # for parentNode in salpB.multiworflow[task[0]][task[1]].inputs:
    #     P = [task[0],parentNode.id]
    #     minMAXIndex = max(minMAXIndex,salpB.Y.index(P))
    # # 子节点任务最小的索引
    # maxMinIndex = inf
    # for parentNode in salpB.multiworflow[task[0]][task[1]].outputs:
    #     P = [task[0],parentNode.id]
    #     maxMinIndex = min(maxMinIndex,salpB.Y.index(P))    
    # InsertPosition = random.randint(minMAXIndex+1,maxMinIndex)
    # salpB.Y.insert(InsertPosition,task)

    position = random.randint(0,len(salpA.X)-1)
    task = salpA.Y[position]
    if salpA.multiworflow[task[0]][task[1]].MI==PRIVATEID: ## yes
        CloudID = PRIVATEID
        r1 = sum(GlobalResource.NUMofPrivateCloudVM)-1
        VmID = random.randint(0,r1)
    else:
        CloudID = random.choice(HYBRIDCLOUD)
        if CloudID ==PRIVATEID:## yes
            r1 = sum(GlobalResource.NUMofPrivateCloudVM)-1
            VmID = random.randint(0,r1)
        else:  ##  yes
            Vmtype = random.randint(0,VMT[CloudID].m-1)
            nums = random.randint(0,EachPBVMTypeNums-1)
            VmID =  EachPBVMTypeNums*Vmtype + nums  # random.randint(0,PBVMNums-1)
    salpA.multiworflow[task[0]][task[1]].VMnum = [CloudID,VmID]
    salpA.X[position] = [CloudID,VmID]


    for i in range(len(salpA.X)):  ##  修订交叉结果，具有隐私属性的任务必须在私有云
        task = salpA.Y[i]
        if (salpA.multiworflow[task[0]][task[1]].MI==PRIVATEID and (salpA.X[i][0]!=PRIVATEID)):
            CloudID = PRIVATEID
            r1 = sum(GlobalResource.NUMofPrivateCloudVM)-1
            VmID = random.randint(0,r1)
            salpA.multiworflow[task[0]][task[1]].VMnum = [CloudID,VmID]
            salpA.X[i] = [CloudID,VmID] 


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

def updatePMPC(Population,front):
    k = len(front[0])
    bestLCS = []
    bestK = [ Population[i] for i in range(k)   ]
    for i in range(k-1):
        L = getLCS(bestK[i].Y, bestK[i+1].Y)
        bestLCS.append(L)
    for i in range(len(Population)):
        for j in range(len(bestLCS)):
            L = getLCS(Population[i].Y, bestLCS[j])
            if L == bestLCS[j]:
                Population[i].pm = 1/(1/Population[i].pm+1)
                Population[i].pc = Population[i].pc - 1/(1/Population[i].pm+1)

def GALCS(): 
    # global  OriginalMWOrder
    popsize = 30
    Deta = 30
    max_iter = 100 
    AlgorithmStart = time.time()
    Population = [ChromosomeInitialization() for g in range(popsize)]
    # MutationRate = 1/len(Population[0].X)
    for iter in range(max_iter):

        non_dominated_sorted_solution = fast_non_dominated_sort(Population)
        CrowdingDistance = crowding_distance(Population,non_dominated_sorted_solution)
        newPopulation = updatePopulation(non_dominated_sorted_solution,CrowdingDistance,Population,popsize)
        non_dominated_sorted_solution = fast_non_dominated_sort(newPopulation)
        CrowdingDistance = crowding_distance(newPopulation,non_dominated_sorted_solution)

        if iter>Deta:
            updatePMPC(newPopulation,non_dominated_sorted_solution)

        for i in range(popsize-1):
            p1 = random.random()
            p2 = random.random()
            if p1<newPopulation[i].pc and p2<newPopulation[i+1].pc:
                Child1,Child2 = crossover(Population[i],Population[i+1])
            if p1<newPopulation[i].pm and p2<newPopulation[i+1].pm:
                Child1,Child2 = mutation(Population[i]),mutation(Population[i+1])           
            newPopulation = newPopulation+[Child1,Child2]
            if time.time() - AlgorithmStart>=1.2*MaxDAGTasks: break
        Population = copy.deepcopy(newPopulation)
        del newPopulation
        AlgorithmEnd = time.time() # AlgorithmStart = time.time()
        AlgorithmRunTime = AlgorithmEnd - AlgorithmStart
        if AlgorithmRunTime>=1.2*MaxDAGTasks: break          
    non_dominated_sorted_solution = fast_non_dominated_sort(Population)
    CrowdingDistance = crowding_distance(Population,non_dominated_sorted_solution)
    newPopulation = updatePopulation(non_dominated_sorted_solution,CrowdingDistance,Population,popsize) 
    non_dominated_sorted_solution = fast_non_dominated_sort(newPopulation)
    CrowdingDistance = crowding_distance(newPopulation,non_dominated_sorted_solution) 
    non_dominated_Solution = [newPopulation[i] for i in non_dominated_sorted_solution[0]] 
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
for times in range(1):
    times = 1
    # for instance in range(len(listWorkflowNum)):
    if True:
        instance = 16
        print('****************\t\t2022_IS_GA\t Running times=%d \t instance=%d \t\t\t****************'%(times,instance))
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



        ## 混合云
        PUBLICID  = 0
        PRIVATEID = 1
        HYBRIDCLOUD = [PUBLICID,PRIVATEID]
        DTT = GlobalResource.DTT #传输时间放大倍数
        VMT = [VMType(),PrivateCloudVMType()]

        NumLevellist = [max([len(tempmultiWorflowDAGLevel[i][j]) for j in range(len(tempmultiWorflowDAGLevel[i]))]) for i in range(len(tempmultiWorflowDAGLevel))] 
        EachPBVMTypeNums = sum(NumLevellist)
        PBVMNums = VMT[PUBLICID].m*EachPBVMTypeNums   # GlobalResource.VMNums
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

        NonDominSalps = GALCS()
        str1 = str(instance)+'_'+str(len(listWorkflowNum[instance]))+'_'+str(MaxDAGTasks)+'_'+str(times)        
        np.save(os.getcwd()+'/GALCS/'+'2022_IS_GALCS_NF-'+str1+'.npy', NonDominSalps)
        print('****************\t\t\t2022_IS_GA\t Running times=%d \t instance=%d \t\t****************'%(times,instance))
