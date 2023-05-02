'''
Created on 15-Mar-2017

@author: itadmin
'''
class Task:
    
    def __init__(self, id, namespace=None, name=None, jobsetname=None, inputs=[], outputs = [],runtime=0, MI=0,):
        self.id = id               #parents=[], storage=0 ,core=None,
        self.name = name
        self.namespace = namespace
        self.jobsetname = jobsetname
        self.runtime = runtime
        self.MI = MI
        # self.storage =  storage
        # self.core = core
        self.inputs =list(inputs)#set(inputs) #
        self.outputs =list(outputs)# set(outputs)#
        # self.currentCompletionTime = 0
        self.VMnum = None
        self.VMcore = None
        self.StartTime = None    # ICPCP  AST    
        self.FinishTime = None     # ICPCP  AST 
        self.EST = None
        self.EFT = None
        self.LFT = None
        self.Assigned = 0
        self.Level = None
        self.SubDeadline = None
        self.XFT = 0

        # self.StatusTable = None


    def addjobsetname(self, jobsetname):
        self.jobsetname = jobsetname

    def addInput(self, file_):
        self.inputs.append(file_) #add(file_)#
    
    def addOutput(self, file_):
        self.outputs.append(file_) #add(file_)#

class DAGTask:    
    def __init__(self, id):
        self.id = id         
        self.VMnum = None
        self.VMcore = None
        self.runtime = 0
        self.StartTime = 0   
        self.FinishTime = 0   
    def __repr__(self):
        return self.id  

# class caculateCmax_Cost():
#     def __init__(self, StartTime,FinishTime):
#         for taskID,task in self.items():

