'''

'''
from xml.dom.minidom import parse
import xml.dom.minidom

import xml.etree.ElementTree as ET
# from Class import *
import random
from Class.Task import Task
from Class.File import File
import copy

KB = 1024
MB = 1024*KB
GB = 1024*MB
TB = 1024*GB

SECONDS = 1
MINUTES = 60*SECONDS
HOURS = 60*MINUTES

MINDATA = 0#99
MAXDATA = 20#1000

MINRUNTIME = 0#999
MAXRUNTIME = 100#5000
class SyntheticGenerator():
    def __init__(self,fileName):
        self.fileName = fileName
   
    def generateSyntheticWorkFlow(self):
        '''
            read testdata 
        '''
        

        tree = ET.parse('./data_SyntheticWorkflows/'+self.fileName)
        root = tree.getroot()

        workFlow =  {}
        for job in root.findall('{http://pegasus.isi.edu/schema/DAX}job'):
            files = job.findall('{http://pegasus.isi.edu/schema/DAX}uses')
            mi = 15000 * float(job.get('runtime'))*SECONDS
            randomRuntime = float(job.get('runtime')) #random.randint(MINRUNTIME, MAXRUNTIME)   #random.randint(50, 99) if random.random()<0.5 else random.randint(5, 49) 
            task = Task(id=int(job.get('id')[2:]), namespace=job.get('namespace'), 
                        name=job.get('name'), runtime=randomRuntime*SECONDS, MI=mi)
            for file in files:
                randomSize = float(file.get('size'))/GB #random.randint(MINDATA, MAXDATA)  # random.randint(10, 20) if random.random()<0.5 else random.randint(1, 9)
                if(file.get('link') == 'output'):
                    tout = File(file.get('file'), size = float(randomSize))#float(file.get('size'))/1024**3
                    task.addOutput(tout)
                if(file.get('link') == 'input'):
                    tin = File(file.get('file'), size = float(randomSize))#float(file.get('size'))/1024**3
                    task.addInput(tin)
            workFlow.update({int(job.get('id')[2:]):task})
              
        for child in root.findall('{http://pegasus.isi.edu/schema/DAX}child'):
            parents =  child.findall('{http://pegasus.isi.edu/schema/DAX}parent')
            if int(child.get('ref')[2:]) in workFlow: 
                child_1 =  workFlow[int(child.get('ref')[2:])].inputs
                for parent in parents:
                    parent_1 =  workFlow[int(parent.get('ref')[2:])].outputs 
                    for each in iter(parent_1):
                        for each1 in iter(child_1):
                            if (each.name == each1.name):
                                each1.booleaninput = True
                                each1.id = int(parent.get('ref')[2:])
                                each.booleanoutput = True
                                each.id = int(child.get('ref')[2:])
                                if each.size != each1.size:
                                    each.size = each1.size

        for each1,each in workFlow.items():            
            while True:  #
                i0 = 0
                for i1 in each.inputs:  
                    if not(i1.booleaninput | i1.booleanoutput):
                        each.inputs.remove(i1)
                        break
                    else:
                        i0 += 1
                if i0 == len(each.inputs):
                    break

            parent_1 = each.inputs        
            for i in range(len(parent_1)-1):  # 
                for j in range(i+1, len(parent_1)):
                    if (parent_1[i].name != None) or (parent_1[j].name != None):
                        if parent_1[i].id == parent_1[j].id:
                            parent_1[j].name = None
                            parent_1[j].booleaninput = False
                            parent_1[i].size = parent_1[i].size + parent_1[j].size                       

            while True: #
                i0 = 0
                for i1 in each.inputs:  
                    if not(i1.booleaninput | i1.booleanoutput):
                        each.inputs.remove(i1)
                        break
                    else:
                        i0 += 1
                if i0 == len(each.inputs):
                    break

            while True:
                i0 = 0
                for i1 in each.outputs:  
                    if not(i1.booleaninput | i1.booleanoutput):
                        each.outputs.remove(i1)
                        break
                    else:
                        i0 += 1
                if i0 == len(each.outputs):
                    break

            child_1 = each.outputs        
            for i in range(len(child_1)-1):  # 
                for j in range(i+1, len(child_1)):
                    if (child_1[i].name != None) or (child_1[j].name != None):
                        if child_1[i].id == child_1[j].id:
                            child_1[j].name = None
                            child_1[j].booleanoutput = False
                            child_1[i].size = child_1[i].size + child_1[j].size   

            while True:
                i0 = 0
                for i1 in each.outputs:  
                    if not(i1.booleaninput | i1.booleanoutput):
                        each.outputs.remove(i1)
                        break
                    else:
                        i0 += 1
                if i0 == len(each.outputs):
                    break     
        for each1,each in workFlow.items(): 
            parent_1 = each.inputs   #  
            for i in range(len(parent_1)):
                child_1 = workFlow[parent_1[i].id].outputs
                boolFlag = True            
                for j in range(len(child_1)):
                    if each1 == child_1[j].id:  #
                        boolFlag = False
                        break
                if boolFlag:
                    strFlag = copy.deepcopy(parent_1[i])
                    strFlag.id = each1
                    strFlag.booleaninput, strFlag.booleanoutput=strFlag.booleanoutput,strFlag.booleaninput
                    workFlow[parent_1[i].id].addOutput(strFlag)

        for each1,each in workFlow.items(): 
            parent_1 = each.outputs   #  
            for i in range(len(parent_1)):
                child_1 = workFlow[parent_1[i].id].inputs
                boolFlag = True            
                for j in range(len(child_1)):
                    if each1 == child_1[j].id:  #parent_1[i].id
                        boolFlag = False
                        break
                if boolFlag:
                    strFlag = copy.deepcopy(parent_1[i])
                    strFlag.id = each1
                    strFlag.booleaninput, strFlag.booleanoutput=strFlag.booleanoutput,strFlag.booleaninput
                    workFlow[parent_1[i].id].addInput(strFlag)        

        return workFlow