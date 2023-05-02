from cmath import inf, sqrt
from numbers import Integral
import os
from sqlalchemy import true
# from pickle import INT  
import xlwings as xw
import GlobalResource
# import GlobalWorkflow


from sys import maxsize
import matplotlib
import matplotlib.pyplot as plt
from math import trunc

from matplotlib.pyplot import close  

from Class.SyntheticGenerator import SyntheticGenerator
import numpy as np
from Class.VMType import PrivateCloudVMType
from Class.File import File
from Class.Task import Task
import math,random
import copy,re,operator
import time
from tqdm import tqdm

# import pygmo #as pg

from pymoo.indicators.hv import HV as HyperVolume 
from pymoo.indicators.igd_plus import IGDPlus
from pymoo.indicators.igd import IGD

''' 评价算法的非支配解集  '''
class ObjectivesNopermutation:
    def __init__(self):
        self.Cost = None #{'Cost':None}
        self.Cmax= None
        self.Energy = None
        self.TotalTardiness = None
        self.NumPBVMs = None
		# ret = re.findall(r"[^\W_]+",MSIAfileName[n])  #  忽略下划线的正则表达式
		# print(ret)


def DelYears(fileName):
    new = []
    for each in fileName:
        new.append(each[each.index('-')+1:-4])
    return new

def maxSR(Solution):
    succ = 0
    for i in range(len(Solution)-1):
        if succ<Solution[i].SuccessfulRate:
            succ = Solution[i].SuccessfulRate
    return succ


readData_Output = True   #     False   #
############################################################################################
if readData_Output:
    '''读数据输出PF'''

    MSIAfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSIA')
    # MSIAfileName.sort()
    MACOfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MACO')
    # MACOfileName.sort()
    GMPSOfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GMPSO')
    # GMPSOfileName.sort()
    GALCSfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GALCS')
    # GALCSfileName.sort()
    HSMfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\HSA9Fs')
    # HSMfileName.sort()  
    MSSA1fileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA1')
    MSSA2fileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA2')
   
    MSIAfileName_NoYears = DelYears(MSIAfileName)
    MACOfileName_NoYears = DelYears(MACOfileName)
    GMPSOfileName_NoYears = DelYears(GMPSOfileName)
    GALCSfileName_NoYears = DelYears(GALCSfileName)
    HSMfileName_NoYears = DelYears(HSMfileName)
    MSSA1fileName_NoYears = DelYears(MSSA1fileName)
    MSSA2fileName_NoYears = DelYears(MSSA2fileName)

    Labels= ['0_3_177_0', '0_3_177_1',#'0_3_177_2','0_3_177_3','0_3_177_4',
            #'0_3_177_5','0_3_177_6','0_3_177_7','0_3_177_8','0_3_177_9',
            '1_3_200_0','1_3_200_1',#'1_3_200_2','1_3_200_3','1_3_200_4',
            #'1_3_200_5','1_3_200_6','1_3_200_7','1_3_200_8','1_3_200_9',
            '2_5_321_0','2_5_321_1',#'2_5_321_2','2_5_321_3','2_5_321_4',
            #'2_5_321_5','2_5_321_6','2_5_321_7','2_5_321_8','2_5_321_9',
            '3_5_429_0','3_5_429_1',#'3_5_429_2','3_5_429_3','3_5_429_4',
            #'3_5_429_5','3_5_429_6','3_5_429_7','3_5_429_8','3_5_429_9',
            '4_7_390_0','4_7_390_1',#'4_7_390_2','4_7_390_3','4_7_390_4',
            #'4_7_390_5','4_7_390_6','4_7_390_7','4_7_390_8','4_7_390_9',
            '5_7_392_0','5_7_392_1',#'5_7_392_2','5_7_392_3','5_7_392_4',
            #'5_7_392_5','5_7_392_6','5_7_392_7','5_7_392_8','5_7_392_9',
            '6_10_649_0','6_10_649_1',#'6_10_649_2','6_10_649_3','6_10_649_4',
            #'6_10_649_5','6_10_649_6','6_10_649_7','6_10_649_8','6_10_649_9',
            '7_10_671_0','7_10_671_1',#'7_10_671_2','7_10_671_3','7_10_671_4',
            #'7_10_671_5','7_10_671_6','7_10_671_7','7_10_671_8','7_10_671_9',
            '8_5_1229_0','8_5_1229_1',#'8_5_1229_2','8_5_1229_3','8_5_1229_4',
            #'8_5_1229_5','8_5_1229_6','8_5_1229_7','8_5_1229_8','8_5_1229_9',
            '9_5_1300_0','9_5_1300_1',#'9_5_1300_2','9_5_1300_3','9_5_1300_4',
            #'9_5_1300_5','9_5_1300_6','9_5_1300_7','9_5_1300_8','9_5_1300_9',
            '10_5_3150_0','10_5_3150_1',#'10_5_3150_2','10_5_3150_3','10_5_3150_4',
            #'10_5_3150_5','10_5_3150_6','10_5_3150_7','10_5_3150_8','10_5_3150_9',
            '11_15_2653_0','11_15_2653_1',#'11_15_2653_2','11_15_2653_3','11_15_2653_4',
            #'11_15_2653_5','11_15_2653_6','11_15_2653_7','11_15_2653_8','11_15_2653_9',
            '12_15_4646_0','12_15_4646_1',#'12_15_4646_2','12_15_4646_3','12_15_4646_4',
            #'12_15_4646_5','12_15_4646_6','12_15_4646_7','12_15_4646_8','12_15_4646_9',
            '13_15_5520_0','13_15_5520_1',#'13_15_5520_2','13_15_5520_3','13_15_5520_4',
            #'13_15_5520_5','13_15_5520_6','13_15_5520_7','13_15_5520_8','13_15_5520_9',
            '14_25_6097_0','14_25_6097_1',#'14_25_6097_2','14_25_6097_3','14_25_6097_4',
            #'14_25_6097_5','14_25_6097_6','14_25_6097_7','14_25_6097_8','14_25_6097_9',
            '15_25_7880_0','15_25_7880_1',#'15_25_7880_2','15_25_7880_3','15_25_7880_4',
            #'15_25_7880_5','15_25_7880_6','15_25_7880_7','15_25_7880_8','15_25_7880_9',
            '16_25_10816_0','16_25_10816_1',#'16_25_10816_2','16_25_10816_3','16_25_10816_4',
            #'16_25_10816_5','16_25_10816_6','16_25_10816_7','16_25_10816_8','16_25_10816_9'
            ]



    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False    # 关闭一些提示信息，可以加快运行速度。 默认为 True。
    app.screen_updating = True    # 更新显示工作表的内容。默认为 True。关闭它也可以提升运行速度。
    book = app.books.add()
    # book = app.books.open(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\test.xlsx')
    sheet = book.sheets.active

    n = 0
    C0,C1,C2,C3 = 0,1,2,3
    for k in tqdm(range(len(Labels)//2)): 
        n_ = 2*k       
        time.sleep(0.1)
        n0 = MSIAfileName_NoYears.index(Labels[n_])
        n2 = GMPSOfileName_NoYears.index(Labels[n_])
        n3 = GALCSfileName_NoYears.index(Labels[n_])
        n4 = HSMfileName_NoYears.index(Labels[n_])
        n5 = MSSA1fileName_NoYears.index(Labels[n_])
        n6 = MSSA2fileName_NoYears.index(Labels[n_]) 
        sheet[k+2, 0+1+0].value = Labels[n_] 
        ret = re.findall(r"[^\W_]+",MSIAfileName[n0]) 
        if int(ret[5])<=1000:  
            n1 = MACOfileName_NoYears.index(Labels[n_])
            MACO = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MACO'+'\\'+MACOfileName[n1],allow_pickle=True)
            sheet[k+2, 0+2+0].value = maxSR(MACO)
        MSIA = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSIA'+'\\'+MSIAfileName[n0],allow_pickle=True)            
        GMPSO = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GMPSO'+'\\'+GMPSOfileName[n2],allow_pickle=True)
        GALCS = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GALCS'+'\\'+GALCSfileName[n3],allow_pickle=True)
        HSA9Fs = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\HSA9Fs'+'\\'+HSMfileName[n4],allow_pickle=True)
        MSSA1 = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA1'+'\\'+MSSA1fileName[n5],allow_pickle=True)
        MSSA2 = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA2'+'\\'+MSSA2fileName[n6],allow_pickle=True)        
        
        sheet[k+2, 0+2+2].value = maxSR(GMPSO)
        sheet[k+2, 0+2+4].value = maxSR(GALCS)
        sheet[k+2, 0+2+6].value = maxSR(MSSA1)
        sheet[k+2, 0+2+8].value = maxSR(MSSA2)
        sheet[k+2, 0+2+10].value = maxSR(HSA9Fs)
        sheet[k+2, 0+2+12].value = maxSR(MSIA)
        n_ += 1
        n0 = MSIAfileName_NoYears.index(Labels[n_])
        n2 = GMPSOfileName_NoYears.index(Labels[n_])
        n3 = GALCSfileName_NoYears.index(Labels[n_])
        n4 = HSMfileName_NoYears.index(Labels[n_])
        n5 = MSSA1fileName_NoYears.index(Labels[n_])
        n6 = MSSA2fileName_NoYears.index(Labels[n_])  
        ret = re.findall(r"[^\W_]+",MSIAfileName[n0]) 
        if int(ret[5])<=1000:  
            n1 = MACOfileName_NoYears.index(Labels[n_])
            MACO = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MACO'+'\\'+MACOfileName[n1],allow_pickle=True)
            sheet[k+2, 1+2+0].value = maxSR(MACO)
        MSIA = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSIA'+'\\'+MSIAfileName[n0],allow_pickle=True)            
        GMPSO = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GMPSO'+'\\'+GMPSOfileName[n2],allow_pickle=True)
        GALCS = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GALCS'+'\\'+GALCSfileName[n3],allow_pickle=True)
        HSA9Fs = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\HSA9Fs'+'\\'+HSMfileName[n4],allow_pickle=True)
        MSSA1 = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA1'+'\\'+MSSA1fileName[n5],allow_pickle=True)
        MSSA2 = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA2'+'\\'+MSSA2fileName[n6],allow_pickle=True)        
        
        sheet[k+2, 1+2+2].value = maxSR(GMPSO)
        sheet[k+2, 1+2+4].value = maxSR(GALCS)
        sheet[k+2, 1+2+6].value = maxSR(MSSA1)
        sheet[k+2, 1+2+8].value = maxSR(MSSA2)
        sheet[k+2, 1+2+10].value = maxSR(HSA9Fs)
        sheet[k+2, 1+2+12].value = maxSR(MSIA)



        n += 1



    
############################################################################################

# AlgorithmNumbers = 5
readData_Output = False   #   True   #  
############################################################################################
if readData_Output:
    '''读数据输出评价结果'''

    # KPI_Name = ['MACO_HV','GMPSO_HV','GALCS_HV','HSM_HV','MSIA_HV',
    #             'MSIA_MACO','MACO_MSIA','MSIA_GMPSO','GMPSO_MSIA','MSIA_GALCS','GALCS_MSIA',
    #             'HSM_MACO','MACO_HSM','HSM_GMPSO','GMPSO_HSM','HSM_GALCS','GALCS_HSM', 'MSIA_HSM','HSM_MSIA',
    #             'MACO_RunTime','GMPSO_RunTime','GALCS_RunTime','HSM_RunTime','MSIA_RunTime',
    #             'MACO_AvgPBVMs','GMPSO_AvgPBVMs','GALCS_AvgPBVMs','HSM_AvgPBVMs','MSIA_AvgPBVMs',
    #             'MACO_IGD','GMPSO_IGD','GALCS_IGD','HSM_IGD','MSIA_IGD'
    #             ]


    MSIAfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSIA')
    # MSIAfileName.sort()
    MACOfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MACO')
    # MACOfileName.sort()
    GMPSOfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GMPSO')
    # GMPSOfileName.sort()
    GALCSfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GALCS')
    # GALCSfileName.sort()
    HSMfileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\HSA9Fs')
    # HSMfileName.sort()    
    MSSA1fileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA1')
    MSSA2fileName=os.listdir(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA2')

    MSIAfileName_NoYears = DelYears(MSIAfileName)
    MACOfileName_NoYears = DelYears(MACOfileName)
    GMPSOfileName_NoYears = DelYears(GMPSOfileName)
    GALCSfileName_NoYears = DelYears(GALCSfileName)
    HSMfileName_NoYears = DelYears(HSMfileName)
    MSSA1fileName_NoYears = DelYears(MSSA1fileName)
    MSSA2fileName_NoYears = DelYears(MSSA2fileName)

    Labels= ['0_3_177_0', '0_3_177_1','0_3_177_2','0_3_177_3','0_3_177_4',
            '0_3_177_5','0_3_177_6','0_3_177_7','0_3_177_8','0_3_177_9',
            '1_3_200_0','1_3_200_1','1_3_200_2','1_3_200_3','1_3_200_4',
            '1_3_200_5','1_3_200_6','1_3_200_7','1_3_200_8','1_3_200_9',
            '2_5_321_0','2_5_321_1','2_5_321_2','2_5_321_3','2_5_321_4',
            '2_5_321_5','2_5_321_6','2_5_321_7','2_5_321_8','2_5_321_9',
            '3_5_429_0','3_5_429_1','3_5_429_2','3_5_429_3','3_5_429_4',
            '3_5_429_5','3_5_429_6','3_5_429_7','3_5_429_8','3_5_429_9',
            '4_7_390_0','4_7_390_1','4_7_390_2','4_7_390_3','4_7_390_4',
            '4_7_390_5','4_7_390_6','4_7_390_7','4_7_390_8','4_7_390_9',
            '5_7_392_0','5_7_392_1','5_7_392_2','5_7_392_3','5_7_392_4',
            '5_7_392_5','5_7_392_6','5_7_392_7','5_7_392_8','5_7_392_9',
            '6_10_649_0','6_10_649_1','6_10_649_2','6_10_649_3','6_10_649_4',
            '6_10_649_5','6_10_649_6','6_10_649_7','6_10_649_8','6_10_649_9',
            '7_10_671_0','7_10_671_1','7_10_671_2','7_10_671_3','7_10_671_4',
            '7_10_671_5','7_10_671_6','7_10_671_7','7_10_671_8','7_10_671_9',
            '8_5_1229_0','8_5_1229_1','8_5_1229_2','8_5_1229_3','8_5_1229_4',
            '8_5_1229_5','8_5_1229_6','8_5_1229_7','8_5_1229_8','8_5_1229_9',
            '9_5_1300_0','9_5_1300_1','9_5_1300_2','9_5_1300_3','9_5_1300_4',
            '9_5_1300_5','9_5_1300_6','9_5_1300_7','9_5_1300_8','9_5_1300_9',
            '10_5_3150_0','10_5_3150_1','10_5_3150_2','10_5_3150_3','10_5_3150_4',
            '10_5_3150_5','10_5_3150_6','10_5_3150_7','10_5_3150_8','10_5_3150_9',
            '11_15_2653_0','11_15_2653_1','11_15_2653_2','11_15_2653_3','11_15_2653_4',
            '11_15_2653_5','11_15_2653_6','11_15_2653_7','11_15_2653_8','11_15_2653_9',
            '12_15_4646_0','12_15_4646_1','12_15_4646_2','12_15_4646_3','12_15_4646_4',
            '12_15_4646_5','12_15_4646_6','12_15_4646_7','12_15_4646_8','12_15_4646_9',
            '13_15_5520_0','13_15_5520_1','13_15_5520_2','13_15_5520_3','13_15_5520_4',
            '13_15_5520_5','13_15_5520_6','13_15_5520_7','13_15_5520_8','13_15_5520_9',
            '14_25_6097_0','14_25_6097_1','14_25_6097_2','14_25_6097_3','14_25_6097_4',
            '14_25_6097_5','14_25_6097_6','14_25_6097_7','14_25_6097_8','14_25_6097_9',
            '15_25_7880_0','15_25_7880_1','15_25_7880_2','15_25_7880_3','15_25_7880_4',
            '15_25_7880_5','15_25_7880_6','15_25_7880_7','15_25_7880_8','15_25_7880_9',
            '16_25_10816_0','16_25_10816_1','16_25_10816_2','16_25_10816_3','16_25_10816_4',
            '16_25_10816_5','16_25_10816_6','16_25_10816_7','16_25_10816_8','16_25_10816_9']



    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False    # 关闭一些提示信息，可以加快运行速度。 默认为 True。
    app.screen_updating = True    # 更新显示工作表的内容。默认为 True。关闭它也可以提升运行速度。
    book = app.books.add()
    # book = app.books.open(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\test.xlsx')
    sheet = book.sheets.active


    
    sheet[0, 0].value= '算法测试'	# 向表test中添加数据
    for i in range(len(KPI_Name)):
        sheet[0, i+1].value= KPI_Name[i]

    n = 0
    for n_ in tqdm(range(len(Labels))):        
        time.sleep(0.1)
        n0 = MSIAfileName_NoYears.index(Labels[n_])
        if ((Labels[n_]in MACOfileName_NoYears) and (Labels[n_]in GMPSOfileName_NoYears) 
            and(Labels[n_]in GALCSfileName_NoYears)):

            n1 = MACOfileName_NoYears.index(Labels[n_])
            n2 = GMPSOfileName_NoYears.index(Labels[n_])
            n3 = GALCSfileName_NoYears.index(Labels[n_])
            n4 = HSMfileName_NoYears.index(Labels[n_])
            n5 = MSSA1fileName_NoYears.index(Labels[n_])
            n6 = MSSA2fileName_NoYears.index(Labels[n_])
            if true:
                MSIA = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSIA'+'\\'+MSIAfileName[n0],allow_pickle=True)
                MACO = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MACO'+'\\'+MACOfileName[n1],allow_pickle=True)
                GMPSO = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GMPSO'+'\\'+GMPSOfileName[n2],allow_pickle=True)
                GALCS = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GALCS'+'\\'+GALCSfileName[n3],allow_pickle=True)
                HSM = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\HSA9Fs'+'\\'+HSMfileName[n4],allow_pickle=True)
                MSSA1 = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA1'+'\\'+MSSA1fileName[n4],allow_pickle=True)
                MSSA2 = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA2'+'\\'+MSSA2fileName[n4],allow_pickle=True)

                AllNF = []
                maxC,maxT,maxE = 0,0,0
                minC,minT,minE = inf,inf,inf
                for i in range(len(MSIA)-1):
                    AllNF.append(MSIA[i])
                for i in range(len(MACO)-1):
                    AllNF.append(MACO[i])
                for i in range(len(GMPSO)-1):
                    AllNF.append(GMPSO[i])
                for i in range(len(GALCS)-1):
                    AllNF.append(GALCS[i])
                for i in range(len(MSSA1)-1):
                    AllNF.append(MSSA1[i])
                for i in range(len(MSSA2)-1):
                    AllNF.append(MSSA2[i])                                        
                # for i in range(len(HSM)-1):
                AllNF.append(HSM[0])
                for each in AllNF:
                    maxC,maxT,maxE = max(each.Cost,maxC),max(each.TotalTardiness,maxT),max(each.Energy,maxE)
                    minC,minT,minE = min(each.Cost,minC),min(each.TotalTardiness,minT),min(each.Energy,minE)

                MSIA_List = sorted(Normalization_NF(MSIA,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                MACO_List = sorted(Normalization_NF(MACO,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                GMPSO_List = sorted(Normalization_NF(GMPSO,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                GALCS_List = sorted(Normalization_NF(GALCS,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                MSSA1_List = sorted(Normalization_NF(MSSA1,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                MSSA2_List = sorted(Normalization_NF(MSSA2,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))                
                HSM_List = sorted(Normalization_NF(HSM,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                AllNF_List = sorted(Normalization_NF(AllNF,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                TruePF = non_dominatedSalps(AllNF)
                TruePF_List = sorted(Normalization_NF(TruePF,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))


                # MSIA_IGDPlus = InvertedGenerationalDistancePlus(MSIA_List,TruePF_List)
                # MACO_IGDPlus = InvertedGenerationalDistancePlus(MACO_List,TruePF_List)
                # GMPSO_IGDPlus = InvertedGenerationalDistancePlus(GMPSO_List,TruePF_List)
                # GALCS_IGDPlus = InvertedGenerationalDistancePlus(GALCS_List,TruePF_List)
                ReferNF_List = [1,1,1]        
                hv = HyperVolume(ref_point = ReferNF_List)
                KPI = {}
                KPI['MSIA_HV'] = hv.do(np.array(MSIA_List))
                KPI['MACO_HV'] = hv.do(np.array(MACO_List))
                KPI['GMPSO_HV'] = hv.do(np.array(GMPSO_List))
                KPI['GALCS_HV'] = hv.do(np.array(GALCS_List)) 
                KPI['MSSA1_HV'] = hv.do(np.array(MSSA1_List)) 
                KPI['MSSA2_HV'] = hv.do(np.array(MSSA2_List)) 
                KPI['HSM_HV'] = hv.do(np.array(HSM_List))  

                KPI['MSIA_IGD'] = InvertedGenerationalDistance(MSIA_List,TruePF_List)
                KPI['MACO_IGD'] = InvertedGenerationalDistance(MACO_List,TruePF_List)
                KPI['GMPSO_IGD'] = InvertedGenerationalDistance(GMPSO_List,TruePF_List)
                KPI['GALCS_IGD'] = InvertedGenerationalDistance(GALCS_List,TruePF_List) 
                KPI['HSM_IGD'] = InvertedGenerationalDistance(HSM_List,TruePF_List)     
                KPI['MSSA1_IGD'] = InvertedGenerationalDistance(MSSA1_List,TruePF_List) 
                KPI['MSSA2_IGD'] = InvertedGenerationalDistance(MSSA2_List,TruePF_List)    

                KPI['MSIA_MACO'] = CoverageRate(MSIA,MACO)
                KPI['MACO_MSIA'] = CoverageRate(MACO,MSIA)

                KPI['MSIA_GMPSO'] = CoverageRate(MSIA,GMPSO)
                KPI['GMPSO_MSIA'] = CoverageRate(GMPSO,MSIA)

                KPI['MSIA_GALCS'] = CoverageRate(MSIA,GALCS)
                KPI['GALCS_MSIA'] = CoverageRate(GALCS,MSIA) 

                KPI['MSIA_MSSA1'] = CoverageRate(MSIA,MSSA1)
                KPI['MSSA1_MSIA'] = CoverageRate(MSSA1,MSIA)

                KPI['MSIA_MSSA2'] = CoverageRate(MSIA,MSSA2)
                KPI['MSSA2_MSIA'] = CoverageRate(MSSA2,MSIA)                

                KPI['HSM_MSSA1'] = CoverageRate(HSM,MSSA1)
                KPI['MSSA1_HSM'] = CoverageRate(MSSA1,HSM)

                KPI['HSM_MSSA2'] = CoverageRate(HSM,MSSA2)
                KPI['MSSA2_HSM'] = CoverageRate(MSSA2,HSM)  

                KPI['HSM_MACO'] = CoverageRate(HSM,MACO)
                KPI['MACO_HSM'] = CoverageRate(MACO,HSM)

                KPI['HSM_GMPSO'] = CoverageRate(HSM,GMPSO)
                KPI['GMPSO_HSM'] = CoverageRate(GMPSO,HSM)

                KPI['HSM_GALCS'] = CoverageRate(HSM,GALCS)
                KPI['GALCS_HSM'] = CoverageRate(GALCS,HSM)    

                KPI['MSIA_HSM'] = CoverageRate(MSIA,HSM)
                KPI['HSM_MSIA'] = CoverageRate(HSM,MSIA)               
   
                KPI['MSIA_RunTime']= MSIA[len(MSIA)-1]['RunTime'] 
                KPI['MACO_RunTime']= MACO[len(MACO)-1]['RunTime'] 
                KPI['GMPSO_RunTime']= GMPSO[len(GMPSO)-1]['RunTime']
                KPI['GALCS_RunTime']= GALCS[len(GALCS)-1]['RunTime'] 
                KPI['MSSA1_RunTime']= MSSA1[len(MSSA1)-1]['RunTime'] 
                KPI['MSSA2_RunTime']= MSSA2[len(MSSA2)-1]['RunTime'] 
                KPI['HSM_RunTime']= HSM[len(HSM)-1]['RunTime'] 

                KPI['MSIA_AvgPBVMs']= MSIA[len(MSIA)-1]['AvgPBVMs']
                KPI['MACO_AvgPBVMs']= MACO[len(MACO)-1]['AvgPBVMs']
                KPI['GMPSO_AvgPBVMs']= GMPSO[len(GMPSO)-1]['AvgPBVMs']
                KPI['GALCS_AvgPBVMs']= GALCS[len(GALCS)-1]['AvgPBVMs']
                KPI['MSSA1_AvgPBVMs']= MSSA1[len(MSSA1)-1]['AvgPBVMs']
                KPI['MSSA2_AvgPBVMs']= MSSA2[len(MSSA2)-1]['AvgPBVMs']
                KPI['HSM_AvgPBVMs']= HSM[len(HSM)-1]['AvgPBVMs']
  
        else:
            ret = re.findall(r"[^\W_]+",MSIAfileName[n0])  #  忽略下划线的正则表达式
            if int(ret[5])>1000:
                if ((Labels[n_]in GMPSOfileName_NoYears) and(Labels[n_]in GALCSfileName_NoYears)): 
                        #(Labels[n_]in MACOfileName_NoYears) and 
                    # n1 = MACOfileName_NoYears.index(Labels[n_])
                    n2 = GMPSOfileName_NoYears.index(Labels[n_])
                    n3 = GALCSfileName_NoYears.index(Labels[n_])
                    n4 = HSMfileName_NoYears.index(Labels[n_])
                    n5 = MSSA1fileName_NoYears.index(Labels[n_])
                    n6 = MSSA2fileName_NoYears.index(Labels[n_])                    
                    if true:
                        MSIA = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSIA'+'\\'+MSIAfileName[n0],allow_pickle=True)
                        # MACO = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MACO'+'\\'+MACOfileName[n1],allow_pickle=True)
                        GMPSO = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GMPSO'+'\\'+GMPSOfileName[n2],allow_pickle=True)
                        GALCS = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\GALCS'+'\\'+GALCSfileName[n3],allow_pickle=True)
                        HSM = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\HSA9Fs'+'\\'+HSMfileName[n4],allow_pickle=True)
                        MSSA1 = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA1'+'\\'+MSSA1fileName[n5],allow_pickle=True)
                        MSSA2 = np.load(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\MSSA2'+'\\'+MSSA2fileName[n6],allow_pickle=True)

                        AllNF = []
                        maxC,maxT,maxE = 0,0,0
                        minC,minT,minE = inf,inf,inf
                        for i in range(len(MSIA)-1):
                            AllNF.append(MSIA[i])
                        # for i in range(len(MACO)-1):
                        #     AllNF.append(MACO[i])
                        for i in range(len(GMPSO)-1):
                            AllNF.append(GMPSO[i])
                        for i in range(len(GALCS)-1):
                            AllNF.append(GALCS[i])
                        for i in range(len(MSSA1)-1):
                            AllNF.append(MSSA1[i])
                        for i in range(len(MSSA2)-1):
                            AllNF.append(MSSA2[i])                              
                        # for i in range(len(HSM)-1):
                        AllNF.append(HSM[0])
                        for each in AllNF:
                            maxC,maxT,maxE = max(each.Cost,maxC),max(each.TotalTardiness,maxT),max(each.Energy,maxE)
                            minC,minT,minE = min(each.Cost,minC),min(each.TotalTardiness,minT),min(each.Energy,minE)

                        MSIA_List = sorted(Normalization_NF(MSIA,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                        # MACO_List = sorted(Normalization_NF(MACO,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                        GMPSO_List = sorted(Normalization_NF(GMPSO,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                        GALCS_List = sorted(Normalization_NF(GALCS,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                        MSSA1_List = sorted(Normalization_NF(MSSA1,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                        MSSA2_List = sorted(Normalization_NF(MSSA2,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))                
                        HSM_List = sorted(Normalization_NF(HSM,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                        AllNF_List = sorted(Normalization_NF(AllNF,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))
                        TruePF = non_dominatedSalps(AllNF)
                        TruePF_List = sorted(Normalization_NF(TruePF,maxC,maxT,maxE,minC,minT,minE),key=operator.itemgetter(0,2))


                        # MSIA_IGDPlus = InvertedGenerationalDistancePlus(MSIA_List,TruePF_List)
                        # MACO_IGDPlus = InvertedGenerationalDistancePlus(MACO_List,TruePF_List)
                        # GMPSO_IGDPlus = InvertedGenerationalDistancePlus(GMPSO_List,TruePF_List)
                        # GALCS_IGDPlus = InvertedGenerationalDistancePlus(GALCS_List,TruePF_List)
                        ReferNF_List = [1,1,1]        
                        hv = HyperVolume(ref_point = ReferNF_List)
                        KPI = {}
                        KPI['MSIA_HV'] = hv.do(np.array(MSIA_List))
                        KPI['MACO_HV'] = ' \ ' # hv.do(np.array(MACO_List))
                        KPI['GMPSO_HV'] = hv.do(np.array(GMPSO_List))
                        KPI['GALCS_HV'] = hv.do(np.array(GALCS_List)) 
                        KPI['MSSA1_HV'] = hv.do(np.array(MSSA1_List)) 
                        KPI['MSSA2_HV'] = hv.do(np.array(MSSA2_List)) 
                        KPI['HSM_HV'] = hv.do(np.array(HSM_List))  

                        KPI['MSIA_IGD'] = InvertedGenerationalDistance(MSIA_List,TruePF_List)
                        KPI['MACO_IGD'] = ' \ ' # InvertedGenerationalDistance(MACO_List,TruePF_List)
                        KPI['GMPSO_IGD'] = InvertedGenerationalDistance(GMPSO_List,TruePF_List)
                        KPI['GALCS_IGD'] = InvertedGenerationalDistance(GALCS_List,TruePF_List) 
                        KPI['HSM_IGD'] = InvertedGenerationalDistance(HSM_List,TruePF_List)        
                        KPI['MSSA1_IGD'] = InvertedGenerationalDistance(MSSA1_List,TruePF_List) 
                        KPI['MSSA2_IGD'] = InvertedGenerationalDistance(MSSA2_List,TruePF_List)    

                        KPI['MSIA_MACO'] = ' \ ' # CoverageRate(MSIA,MACO)
                        KPI['MACO_MSIA'] = ' \ ' # CoverageRate(MACO,MSIA)

                        KPI['MSIA_GMPSO'] = CoverageRate(MSIA,GMPSO)
                        KPI['GMPSO_MSIA'] = CoverageRate(GMPSO,MSIA)

                        KPI['MSIA_GALCS'] = CoverageRate(MSIA,GALCS)
                        KPI['GALCS_MSIA'] = CoverageRate(GALCS,MSIA) 

                        KPI['MSIA_MSSA1'] = CoverageRate(MSIA,MSSA1)
                        KPI['MSSA1_MSIA'] = CoverageRate(MSSA1,MSIA)

                        KPI['MSIA_MSSA2'] = CoverageRate(MSIA,MSSA2)
                        KPI['MSSA2_MSIA'] = CoverageRate(MSSA2,MSIA)                

                        KPI['HSM_MSSA1'] = CoverageRate(HSM,MSSA1)
                        KPI['MSSA1_HSM'] = CoverageRate(MSSA1,HSM)

                        KPI['HSM_MSSA2'] = CoverageRate(HSM,MSSA2)
                        KPI['MSSA2_HSM'] = CoverageRate(MSSA2,HSM)  

                        KPI['HSM_MACO'] = ' \ ' # CoverageRate(HSM,MACO)
                        KPI['MACO_HSM'] =' \ ' #  CoverageRate(MACO,HSM)

                        KPI['HSM_GMPSO'] = CoverageRate(HSM,GMPSO)
                        KPI['GMPSO_HSM'] = CoverageRate(GMPSO,HSM)

                        KPI['HSM_GALCS'] = CoverageRate(HSM,GALCS)
                        KPI['GALCS_HSM'] = CoverageRate(GALCS,HSM)    

                        KPI['MSIA_HSM'] = CoverageRate(MSIA,HSM)
                        KPI['HSM_MSIA'] = CoverageRate(HSM,MSIA)               
        
                        KPI['MSIA_RunTime']= MSIA[len(MSIA)-1]['RunTime'] 
                        KPI['MACO_RunTime']= ' \ ' # MACO[len(MACO)-1]['RunTime'] 
                        KPI['GMPSO_RunTime']= GMPSO[len(GMPSO)-1]['RunTime']
                        KPI['GALCS_RunTime']= GALCS[len(GALCS)-1]['RunTime'] 
                        KPI['MSSA1_RunTime']= MSSA1[len(MSSA1)-1]['RunTime'] 
                        KPI['MSSA2_RunTime']= MSSA2[len(MSSA2)-1]['RunTime']                        
                        KPI['HSM_RunTime']= HSM[len(HSM)-1]['RunTime'] 

                        KPI['MSIA_AvgPBVMs']= MSIA[len(MSIA)-1]['AvgPBVMs']
                        KPI['MACO_AvgPBVMs']= ' \ ' # MACO[len(MACO)-1]['AvgPBVMs']
                        KPI['GMPSO_AvgPBVMs']= GMPSO[len(GMPSO)-1]['AvgPBVMs']
                        KPI['GALCS_AvgPBVMs']= GALCS[len(GALCS)-1]['AvgPBVMs']
                        KPI['MSSA1_AvgPBVMs']= MSSA1[len(MSSA1)-1]['AvgPBVMs']
                        KPI['MSSA2_AvgPBVMs']= MSSA2[len(MSSA2)-1]['AvgPBVMs']                        
                        KPI['HSM_AvgPBVMs']= HSM[len(HSM)-1]['AvgPBVMs']                        
        n += 1
        sheet[n, 0].value =  Labels[n_]
        for i in range(len(KPI_Name)):
            sheet[n, i+1].value= KPI[KPI_Name[i]]      
                
        ''' 优值标注'''      
        AlgorithmNumbers = 7
        '''max'''
        HV_List = [sheet[n, i+1].value for i in range(AlgorithmNumbers)]
        HV_List[0] = -inf if HV_List[0]== ' \ ' else  HV_List[0]
        for i in range(AlgorithmNumbers):
            if sheet[n, i+1].value == max(HV_List):
                sheet[n, i+1].api.Font.Color = 0x0000ff #red
                sheet[n, i+1].api.Font.Bold = True
                sheet[n, i+1].api.Font.Italic = True       
        
        
        CR_Num = (AlgorithmNumbers-2)*2+1
        start_num = KPI_Name.index('MSIA_MACO')
        for each in range(CR_Num):
            if sheet[n, start_num+1+each*2].value > sheet[n, start_num+1+1+each*2].value:
                sheet[n, start_num+1+each*2].api.Font.Color = 0x0000ff
                sheet[n, start_num+1+each*2].api.Font.Bold = True
                sheet[n, start_num+1+each*2].api.Font.Italic = True            
            elif sheet[n, start_num+1+each*2].value < sheet[n, start_num+1+1+each*2].value:
                sheet[n, start_num+1+1+each*2].api.Font.Color = 0x0000ff
                sheet[n, start_num+1+1+each*2].api.Font.Bold = True
                sheet[n, start_num+1+1+each*2].api.Font.Italic = True
        '''min'''
        minNum = 3
        start_num = KPI_Name.index('MACO_RunTime')
        for each in [0]:# range(minNum) ## 运行时间 第二小的加粗
            HV_List = [sheet[n, start_num+1+i+each*AlgorithmNumbers].value for i in range(AlgorithmNumbers)]
            HV_List[0] = inf if HV_List[0]== ' \ ' else  HV_List[0]
            min2 = sorted(HV_List)[1]
            for i in range(AlgorithmNumbers):
                if HV_List[i] <= min2:
                    sheet[n, start_num+1+i+each*AlgorithmNumbers].api.Font.Color = 0x0000ff #red
                    sheet[n, start_num+1+i+each*AlgorithmNumbers].api.Font.Bold = True  
                    sheet[n, start_num+1+i+each*AlgorithmNumbers].api.Font.Italic = True              
        for each in range(1,minNum):
            HV_List = [sheet[n, start_num+1+i+each*AlgorithmNumbers].value for i in range(AlgorithmNumbers)]
            HV_List[0] = inf if HV_List[0]== ' \ ' else  HV_List[0]
            for i in range(AlgorithmNumbers):
                if HV_List[i] == min(HV_List):
                    sheet[n, start_num+1+i+each*AlgorithmNumbers].api.Font.Color = 0x0000ff #red
                    sheet[n, start_num+1+i+each*AlgorithmNumbers].api.Font.Bold = True  
                    sheet[n, start_num+1+i+each*AlgorithmNumbers].api.Font.Italic = True            





    book.save(r'D:\OneDrive - kust.edu.cn\Ph.D\Procedure\Three\Results\SuccessfulRate\test-Revise.xlsx')
    book.close()
    app.quit()
k = 1
