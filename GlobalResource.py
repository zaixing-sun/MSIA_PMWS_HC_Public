from pyclbr import Function
from typing import Sequence
import os
import numpy as np
from numpy.core.fromnumeric import mean
from Class.VMType import VMType,PrivateCloudVMType
# from Class.PrivateCloudVMType import PrivateCloudVMType
import math
import copy
from Class.Task import Task
from Class.File import File
import operator

class Objectives:
    def __init__(self):
        self.Cost = None #{'Cost':None}
        self.Cmax= None #{'Cmax':None}
        self.ResourceUtilization = None #{'ResourceUtilization':None}
        self.NoHiberCost = None #{'NoHiberCost':None}
        self.AlgorithmRunTime = None #{'AlgorithmRunTime':None}
        self.NC = None #{'NC':None}
        self.Speedup = None #{'Speedup':None}
        self.SLR = None #{'SLR':None}
        self.ART = None #{'ART':None}
        self.Energy = None
        self.missDDL = None
        self.TotalTardiness = None 


def SimplifyVMS(VMS):
    k = 0
    while True:
        if k >=len(VMS):
            break
        if max(VMS[k].CompleteTime)==0:
            del VMS[k]
            k = 0
        else:
            k += 1
    return VMS
 

def caculateMultiWorkflowMakespan_Cost(resultWorkflow,WfDeadline,VMS):
    PUBLICID  = 0
    PRIVATEID = 1
    HYBRIDCLOUD = [PUBLICID,PRIVATEID]
    VMT = [VMType(),PrivateCloudVMType()]

    Obj = Objectives()
    Obj.Cmax = 0 # AWSCOLDSTARTUP  # Cmax 加上启动时间
    for CloudID in HYBRIDCLOUD:
        VMNums = len(VMS[CloudID])        
        for VMnumID in range(VMNums):
            TaskCoreID = 0
            if len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])>0:                 
                taskID = len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID]) - 1
                FinishTime = VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]  # 此处默认为单核执行
                if Obj.Cmax<FinishTime:
                    Obj.Cmax = FinishTime
    Obj.Cmax += AWSCOLDSTARTUP

    Obj.Cost = 0
    TTT = 1 # 1024*1024
    CloudID = PUBLICID
    VMNums = len(VMS[CloudID])        
    for VMnumID in range(VMNums):                    
        ProcessingTasks = False
        for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores):
            if len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])>0:
                ProcessingTasks = True
                break 
        if ProcessingTasks:
            for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores) :       
                time0 = AWSCOLDSTARTUP
                HStart0 = 0                   
                for taskID in range(len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])):
                    task = VMS[CloudID][VMnumID].TaskCore[TaskCoreID][taskID]
                    TransOUT = 0
                    for sucTask in resultWorkflow[task[0]][task[1]].outputs:                                
                        if resultWorkflow[task[0]][sucTask.id].VMnum[0]==PRIVATEID:
                            TransOUT += sucTask.size                           
                    Obj.Cost += (TransOUT/TTT * VMT[CloudID].price_trans_data['OUT'])  # TransIN/TTT * VMT[CloudID].price_trans_data['IN'] +


                    taskRunTime = VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]
                    time0 += taskRunTime
                    # totalRuntimeofTasks += taskRunTime
                    # tatalData += resultWorkflow[task[0]][task[1]].runtime
                    if taskID==0:
                        IdleTime = 0
                    else:
                        IdleTime = VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID-1][1]
                    if  (taskID>0) and(VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID-1][1]-HStart0>HibernateInterval)and(IdleTime> HibernateLowerBound ): 
                        HibernateTime = IdleTime - AWSWARMSTARTUP

                        Obj.Cost += max(math.ceil(time0)/INTERVAL,60) * (VMT[CloudID].M[VMS[CloudID][VMnumID].id  ] /3600 *INTERVAL)
                        Obj.Cost += max(math.ceil(HibernateTime)/INTERVAL,60) * (ElasticIP /3600 *INTERVAL)
                        time0 = AWSWARMSTARTUP
                        HStart0 = VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]
                        continue
                Obj.Cost += max(math.ceil(time0)/INTERVAL,60) * (VMT[CloudID].M[VMS[CloudID][VMnumID].id] /3600 *INTERVAL)
                # Obj.Cost += (tatalData/TTT * VMT[CloudID].price_store_data)

    Obj.Energy = 0
    totalTransEnergy = 0
    for dagNum in range(len(resultWorkflow)):
        for taskId in range(len(resultWorkflow[dagNum])):
            VMnum = resultWorkflow[dagNum][taskId].VMnum
            ## 计算传出数据能耗
            for sucTask in resultWorkflow[dagNum][taskId].outputs: 
                sucVMnum = resultWorkflow[dagNum][sucTask.id].VMnum
                if (VMnum == sucVMnum)or((VMnum[0]==PUBLICID)and(sucVMnum[0]==PUBLICID)):
                    DataTransferTime = 0
                else:                      
                    DataTransferRate = min(VMT[VMnum[0]].B[VMS[VMnum[0]][VMnum[1]].id],  VMT[sucVMnum[0]].B[VMS[sucVMnum[0]][sucVMnum[1]].id]   )
                    DataTransferTime = (sucTask.size/DataTransferRate * DTT)  #将传输时间放大DTT倍 
                totalTransEnergy += DataTransferTime/3600*VMT[PRIVATEID].trans_power
    totalIdleEnergy = 0
    totalDynaEnergy = 0
    CloudID = PRIVATEID
    VMNums = len(VMS[CloudID])        
    for VMnumID in range(VMNums):                               #VM层
        ProcessingTasks = False
        for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores):
            if len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])>0:
                ProcessingTasks = True
                break 
        if ProcessingTasks:
            totalRuntimeofTasks = 0 
            for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores) :     #VM的核层  
                for taskID in range(len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])):
                    totalRuntimeofTasks += VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]
            tatalIdleTime = Obj.Cmax - totalRuntimeofTasks
            totalDynaEnergy = totalRuntimeofTasks/3600*VMT[CloudID].dynamic_power[VMS[CloudID][VMnumID].id] 
            totalIdleEnergy = tatalIdleTime/3600* VMT[CloudID].idle_power[VMS[CloudID][VMnumID].id]
    Obj.Energy = totalTransEnergy + totalIdleEnergy + totalDynaEnergy

    # Obj.TotalTardiness = 0
    Tardiness = [] # [0 for i in range(len(resultWorkflow))]
    for i in range(len(resultWorkflow)):
        Cmax = 0
        for j in range(len(resultWorkflow[i])):
            Cmax = max(Cmax,resultWorkflow[i][j].FinishTime)
        temp = max(0,Cmax-WfDeadline[i]) # +AWSCOLDSTARTUP
        Tardiness.append(temp)
    Obj.TotalTardiness = sum(Tardiness)
    ############################################################
    ##  20230336  算法的成功率：非劣解集中存在一个
    missDDL = 0 # 统计成功的个数
    Obj.SLR = []
    for i in range(len(resultWorkflow)):
        Cmax = 0
        for j in range(len(resultWorkflow[i])):
            Cmax = max(Cmax,resultWorkflow[i][j].FinishTime)
        Obj.SLR.append([Cmax,WfDeadline[i]])
        if Cmax-WfDeadline[i]>0:
            missDDL += 1
    Obj.missDDL = 1- missDDL/len(resultWorkflow)   # sum(missDDL)    
    return Obj 

def DetermineWhether2Dominate(salpA,salpB): ## Cost   Energy   TotalTardiness
    ''' salpA 可支配 salpB  '''
    if ((salpA.objectives.Cost<=salpB.objectives.Cost) and(salpA.objectives.Energy<=salpB.objectives.Energy)
            and(salpA.objectives.TotalTardiness<=salpB.objectives.TotalTardiness)):
        if ((salpA.objectives.Cost<salpB.objectives.Cost) or (salpA.objectives.Energy<salpB.objectives.Energy)
             or (salpA.objectives.TotalTardiness<salpB.objectives.TotalTardiness)):
            return True
    return False

def DetermineWhether2Equal(salpA,salpB): ## Cost   Energy   TotalTardiness
    ''' salpA 等于 salpB  '''
    if ((salpA.objectives.Cost==salpB.objectives.Cost) and(salpA.objectives.Energy==salpB.objectives.Energy)
            and(salpA.objectives.TotalTardiness==salpB.objectives.TotalTardiness)):
        return True  # 包含相等的
    return False


# global workflow 0 Montage 100.xml  .xml  .xml  Epigenomics_24.xml   CyberShake_30.xml   
# WorkFlowTestName = 'Montage_25'   #  CyberShake_100  Inspiral_30   Sipht_30                
DTT = 1                 # 传输时间放大倍数 00
PUBLICID  = 0
PRIVATEID = 1
# VMNums = 2 * len(VMType().ProcessingCapacity)  # 10             # VM的数量  假设可供选择的VM总量为类型的整数倍即 5 10 15 20...
# minECU = min(VMType().ProcessingCapacity)  # 10             # min ProcessingCapacity
# maxECU = max(VMType().ProcessingCapacity)
# minB = min(VMType().B)  # 1                # min 内网带宽
# maxB = max(VMType().B)

def STARTUP(CloudID):
    if CloudID==PUBLICID:
        return AWSCOLDSTARTUP
    else:
        return 0


minECU = min(PrivateCloudVMType().ProcessingCapacity)  # 10             # min ProcessingCapacity
maxECU = max(PrivateCloudVMType().ProcessingCapacity)
minB = min(PrivateCloudVMType().B)  # 1                # min 内网带宽
maxB = max(PrivateCloudVMType().B)
NUMofPrivateCloudVM = [3,3,4]   #[1,1,1] # 不能为0   [0 for i in PrivateCloudVMType().P]



ObjectiveNumbers = ['Cost','ResourceUtilization','NoHiberCost','AlgorithmRunTime']
AlgorithmNumbers = 5
ReferenceProcessingCapacity = VMType().ProcessingCapacity[1]

HibernateLowerBound = 60 # 启动休眠的最低限制
AWSCOLDSTARTUP = 55.9  # [2021 启动时间] An Empirical Analysis of VM Startup Times in Public IaaS Clouds An Extended Report
AWSWARMSTARTUP = 34.0
AWSSTOPPING = 5.6 
INTERVAL = 1 # 计费时间间隔，单位：秒   # 60 # 更改为60s 原因是每次启动后，最低收取一分钟费用。   
ElasticIP = 0.005   # Elastic IP (EIP)  您可以免费将一个 Elastic IP (EIP) 地址与运行的实例相关联。
                    # 如果将其他 EIP 与该实例关联，则需要按比例对每小时与该实例关联的其他 EIP 付费。
                    # 0.005 USD（按比例每小时与正在运行的实例相关联的额外 IP 地址）
SuitVM = 1                    
HibernateInterval = 120 
repeatTmies = 10


listWorkflowNum = np.load(os.getcwd()+'/FininaltestInstanceIndex.npy',allow_pickle=True)
# FininaltestInstanceIndex = []
# listWorkflowNum2 = np.load(os.getcwd()+'\\testInstanceIndex_Lessthan1000.npy',allow_pickle=True) # 
# list2 = [3,0,7,6,9,10,15,14]
# for i in list2:
#     FininaltestInstanceIndex.append(listWorkflowNum2[i])
# listWorkflowNum = np.load(os.getcwd()+'\\testInstanceIndex.npy',allow_pickle=True) # _Lessthan1000
# list0 = [0,3,1,11,9,10,18,19,16]
# for i in list0:
#     FininaltestInstanceIndex.append(listWorkflowNum[i])
# np.save(os.getcwd()+'\\FininaltestInstanceIndex.npy', FininaltestInstanceIndex)
# k = 1


# def _init():
#     global _global_dict
#     _global_dict = {}
 
def set_globalvalue(name, value):
    _global_dict[name] = value
 
def get_globalvalue(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue
_global_dict = {}



class ObjectivesNopermutation:
    def __init__(self):
        self.Cost = None #{'Cost':None}
        self.Cmax= None
        self.Energy = None
        self.TotalTardiness = None
        self.CmaxDeadline = None
        self.SuccessfulRate = None
        self.NumPBVMs = None


def RemovePermutation(tempPF):
    PF = []
    PBVMs = []
    '''NF '''
    for i in range(len(tempPF)-1):
        Obj = ObjectivesNopermutation()
        Obj.Cost =  tempPF[i].objectives.Cost
        Obj.Cmax =  tempPF[i].objectives.Cmax
        Obj.Energy =  tempPF[i].objectives.Energy
        Obj.TotalTardiness =  tempPF[i].objectives.TotalTardiness
        Obj.CmaxDeadline =  tempPF[i].objectives.SLR 
        Obj.SuccessfulRate =  tempPF[i].objectives.missDDL       

        Obj.NumPBVMs = 0
        TaskCoreID = 0
        for CloudID in [0]: # ,1
            VMnum = len(tempPF[i].VMSchedule[CloudID])
            for VMnumID in range(VMnum):
                if tempPF[i].VMSchedule[CloudID][VMnumID].CompleteTime[TaskCoreID]>0:
                    Obj.NumPBVMs += 1
        PBVMs.append(Obj.NumPBVMs)
        PF.append(Obj)
    PF.append({'RunTime':tempPF[len(tempPF)-1], 'AvgPBVMs':math.trunc(np.average(PBVMs))})
    return PF

