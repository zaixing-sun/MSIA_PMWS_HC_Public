'''  清洗原有的数据结果'''
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

import time
from tqdm import tqdm

####################  读取非劣解集 .npy文件    ####################################
class SalpClass:   #  szx
    def __init__(self):
        self.ContiSalp=None
        self.DiscrSalp=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.LevelTask=None

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
        self.VMOrder=None
        self.TasksOrder=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None

class ObjectivesNopermutation:
    def __init__(self):
        self.Cost = None #{'Cost':None}
        self.Cmax= None
        self.Energy = None
        self.TotalTardiness = None
        self.NumPBVMs = None

### 地址 1 
# listfileName=os.listdir(os.getcwd()+'\\ParetoFrontNoPermutation') 
# for fileName in listfileName:
#     tempPF = np.load(os.getcwd()+'\\ParetoFrontNoPermutation\\'+fileName,allow_pickle=True) #  ParetoFront
##  地址 2 
listfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\HSM') 
for fileName in tqdm(listfileName):
    # fileName = '2022_HSM_NF-0_5_1229_0.npy'
    tempPF = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\HSM'+'\\'+fileName,allow_pickle=True)
    PF = []
    PBVMs = []
    ''' one solution'''
    Obj = ObjectivesNopermutation()
    Obj.Cost =  tempPF[0].objectives.Cost
    Obj.Cmax =  tempPF[0].objectives.Cmax
    Obj.Energy =  tempPF[0].objectives.Energy
    Obj.TotalTardiness =  tempPF[0].objectives.TotalTardiness 
    Obj.NumPBVMs = 0
    TaskCoreID = 0
    for CloudID in [0]: # ,1
        VMnum = len(tempPF[0].VMSchedule[CloudID])
        for VMnumID in range(VMnum):
            if tempPF[0].VMSchedule[CloudID][VMnumID].CompleteTime[TaskCoreID]>0:
                Obj.NumPBVMs += 1
    PBVMs.append(Obj.NumPBVMs)
    PF.append(Obj)
    PF.append({'RunTime':tempPF[0].objectives.AlgorithmRunTime, 'AvgPBVMs':math.trunc(np.average(PBVMs))})
    # PF.append({'RunTime':tempPF[len(tempPF)-1], 'AvgPBVMs':math.trunc(np.average(PBVMs))})    

    '''NF '''
    # for i in range(len(tempPF)-1):
    #     Obj = ObjectivesNopermutation()
    #     Obj.Cost =  tempPF[i].objectives.Cost
    #     Obj.Cmax =  tempPF[i].objectives.Cmax
    #     Obj.Energy =  tempPF[i].objectives.Energy
    #     Obj.TotalTardiness =  tempPF[i].objectives.TotalTardiness
        
        
    #     Obj.NumPBVMs = 0
    #     TaskCoreID = 0
    #     for CloudID in [0]: # ,1
    #         VMnum = len(tempPF[i].VMSchedule[CloudID])
    #         for VMnumID in range(VMnum):
    #             if tempPF[i].VMSchedule[CloudID][VMnumID].CompleteTime[TaskCoreID]>0:
    #                 Obj.NumPBVMs += 1
    #     PBVMs.append(Obj.NumPBVMs)
    #     PF.append(Obj)
    # PF.append({'RunTime':tempPF[len(tempPF)-1], 'AvgPBVMs':math.trunc(np.average(PBVMs))})

    np.save(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\HSM'+'\\'+fileName,PF)
    time.sleep(0.1)
print('All Done')


