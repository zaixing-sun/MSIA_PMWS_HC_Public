'''

    H. Topcuoglu, S. Hariri and Min-You Wu, 
    "Performance-effective and low-complexity task scheduling for heterogeneous computing," 
    in IEEE Transactions on Parallel and Distributed Systems, 
    vol. 13, no. 3, pp. 260-274, March 2002, doi: 10.1109/71.993206.


    Randomly Generated Application Graphs
        
'''  

import os 
from numpy.lib.function_base import append, copy
# from Class.VMScheduling import VMScheduling
# import Class.SyntheticGenerator
# import Class.VMType

# from File import File
# from Task import Task #,DAGTask


from Class.File import File
from Class.Task import Task #,DAGTask


# import string
import math
import numpy as np
import copy
import random
import matplotlib.pyplot as plt 
import GlobalResource
import networkx as nx


# NUM_TASKS = 6 # 10          # Number of tasks in the graph, (v)
ALPHA = 1             # Shape parameter of the graph, (α)
OUT_DGREE = 4           # Out degree of a node, (out_degree)
CCR = 0.5               # Communication to computation ratio, (CCR).
BATA = 0.25             # Range percentage of computation costs on processors, (β).
JUMP = 4                # indicates that an edge can go from level l to level l þ jump.
RAND_MAX = 0x7fff
MINDATA = 1800            # minimum data size  2048
MAXDATA = 180000          # maximum data size
DENSITY = 10           # determines the number of edges between two levels of the DAG

superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

class RandomlyGeneratedApplicationGraphs():

    def generateWorkflow():
        workflow = {i:Task(i,runtime=random.randint(MINDATA,MAXDATA)) for i in range(NUM_TASKS)}
        '''
        数据量为1024*rand(2048,204800)字节

        tasks_per_level:每层的任务
        nb_tasks：每层任务的个数
        nb_level_task：每个任务所在的层
        '''
    
        #   /* Generating all the tasks */
        tasks_per_level,nb_tasks,nb_level_task = generateTasks(workflow)

        #   /* Generating the Dependencies */
        generateDependencies(workflow,tasks_per_level)

        MET = getMET(workflow)
        EST,EFT = getEST(workflow,MET)
        Deadline = max(EFT)
        DeadlineFactor = 1.1
        workflow['Deadline'] = math.trunc(Deadline*DeadlineFactor)
        workflow['DeadlineFactor'] = DeadlineFactor

        drawDAG(workflow,nb_tasks)

        return workflow

    def GeneratedGaussianEliminationAlgorithm():
        tasks = []
        for k in range(NUM_TASKS-1):
            for j in range(k,NUM_TASKS):
                tasks.append((k,j))
        workflow = {i:Task(i,runtime=random.randint(MINDATA,MAXDATA)) for i in range(len(tasks))}

        for i in range(len(tasks)):
            if tasks[i][0]==tasks[i][1]:
                for j in range(tasks[i][0]+1,NUM_TASKS):
                    child = File(tasks.index((tasks[i][0],j)), id=tasks.index((tasks[i][0],j)),
                                size = random.randint(MINDATA/100,MAXDATA/100), booleanoutput=True)
                    workflow[i].outputs.append(child)

                    parent = File(i, id=i,size = child.size, booleaninput=True)
                    workflow[tasks.index((tasks[i][0],j))].inputs.append(parent)

                    # G.add_edge(i, tasks.index((tasks[i][0],j)) )
            elif tasks[i][0]<NUM_TASKS-2:
                child = File(tasks.index((tasks[i][0]+1,tasks[i][1])), id=tasks.index((tasks[i][0]+1,tasks[i][1])),
                                size = random.randint(MINDATA/100,MAXDATA/100), booleanoutput=True)
                workflow[i].outputs.append(child)

                parent = File(i, id=i,size = child.size, booleaninput=True)
                workflow[tasks.index((tasks[i][0]+1,tasks[i][1]))].inputs.append(parent)
                # G.add_edge(i, tasks.index((tasks[i][0]+1,tasks[i][1])) )

        # MET = getMET(workflow)
        # EST,EFT = getEST(workflow,MET)
        # Deadline = max(EFT)
        # DeadlineFactor = 1.1
        # workflow['Deadline'] = math.trunc(Deadline*DeadlineFactor)
        # workflow['DeadlineFactor'] = DeadlineFactor

        G = nx.DiGraph()    
        options = {"with_labels": True, "node_color": "white", "edgecolors": "black"}
        pos = []    
        node_colors = []
        colors = ['red', 'orange', 'gold', 'lawngreen', 'lightseagreen', 'royalblue','blueviolet']
        k = 0
        for i in range(len(tasks)):
            G.add_node(i)  #,desc='$T_{'+str(i+1)+'}$' 
            node_colors.append(colors[tasks[i][0]%len(colors)])

            pos.append(((tasks[i][0]+k)*0.5,tasks[i][1]*0.5))
            if tasks[i][0]==tasks[i][1]: k+=1

        for i in range(len(tasks)):
            if tasks[i][0]==tasks[i][1]:
                for j in range(tasks[i][0]+1,NUM_TASKS):
                    G.add_edge(i, tasks.index((tasks[i][0],j)) )
            elif tasks[i][0]<NUM_TASKS-2:
                G.add_edge(i, tasks.index((tasks[i][0]+1,tasks[i][1])) )
        # 画出标签
        node_labels = nx.get_node_attributes(G, 'desc') 
        nx.draw(G, pos, labels=node_labels,width= 0.25,node_size=100, **options) # 加颜色,node_color=node_colors
        # 画出边权值
        # edge_labels = nx.get_edge_attributes(G, 'name')
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,width= 0.25)
            # , node_size =20
        plt.title('DAG', fontsize=10)
        plt.show()

        return workflow

    def MolecularDynamicsCode():
        edge = [(0,1),(0,2),(0,3),(1,4),(1,6),              (2,5),(2,6),(3,7),(3,8),(3,9),
                (3,10),(4,11),(5,11),(6,12),(6,27),         (6,28),(7,13),(8,13),(9,14),(10,14),
                (11,15),(11,16),(11,17),(11,18),(11,19),    (11,20),(12,15),(12,16),(12,17),(12,18),
                (12,19),(12,20),(13,20),(13,21),(14,21),    (15,22),(15,23),(15,24),(16,25),(17,25),
                (18,25),(18,26),(19,26),(20,26),(20,33),    (21,27),(21,28),(22,29),(23,29),(23,30),
                (24,30),(24,31),(25,32),(26,32),(27,31),    (27,32),(27,34),(28,33),(28,34),(29,35),
                (30,35),(31,36),(32,36),(33,37),(34,37),    (35,38),(36,38),(36,39),(37,39),(38,40),
                (39,40)]
        TotalTask = 41
        workflow = {i:Task(i, runtime=random.randint(MINDATA,MAXDATA)) for i in range(TotalTask)}
        nb_tasks = [1,3,7,4,7,7,6,3,2,1]  # 每层任务的个数
        nb_tasks0 = [0,0,0,0,0,0,0,0,0,0]    
        k = 0
        i = 0
        while k<TotalTask:
            if nb_tasks0[i]<nb_tasks[i]:
                workflow[k].name = i
                k += 1
                nb_tasks0[i] += 1
            else:
                i += 1
        for i,j in edge:
            size_temp = random.randint(MINDATA/100,MAXDATA/100)
            child = File(j,id=j,size = size_temp,booleanoutput=True)
            workflow[i].outputs.append(child)

            parent = File(i,id=i,size = size_temp,booleaninput=True)
            workflow[j].inputs.append(parent)

        # 生成问题时要注释
        MET = getMET(workflow)
        EST,EFT = getEST(workflow,MET)
        Deadline = max(EFT)
        DeadlineFactor = 1.1
        workflow['Deadline'] = math.trunc(Deadline*DeadlineFactor)
        workflow['DeadlineFactor'] = DeadlineFactor

        drawDAG(workflow,nb_tasks)

        return workflow

    def RandomDAG_10():
        edge = [(0,1),(0,2),(0,3),(0,4),
                (1,5),(2,5),(2,6),(3,6),(4,7),                
                (5,8),(6,8),(7,8)]
        TotalTask = 9
        workflow = {i:Task(i, runtime=random.randint(MINDATA,MAXDATA)) for i in range(TotalTask)}
        nb_tasks = [1,4,3,1]  # 每层任务的个数
        nb_tasks0 = [0,0,0,0]    
        k = 0
        i = 0
        while k<TotalTask:
            if nb_tasks0[i]<nb_tasks[i]:
                workflow[k].name = i
                k += 1
                nb_tasks0[i] += 1
            else:
                i += 1
        for i,j in edge:
            size_temp = random.randint(MINDATA/100,MAXDATA/100)
            child = File(j,id=j,size = size_temp,booleanoutput=True)
            workflow[i].outputs.append(child)

            parent = File(i,id=i,size = size_temp,booleaninput=True)
            workflow[j].inputs.append(parent)

        MET = getMET(workflow)
        EST,EFT = getEST(workflow,MET)
        Deadline = max(EFT)
        DeadlineFactor = 1.1
        workflow['Deadline'] = math.trunc(Deadline*DeadlineFactor)
        workflow['DeadlineFactor'] = DeadlineFactor

        # drawDAG(workflow,nb_tasks)

        return workflow

    def RandomDAG_L2():
        edge = [(0,1)]
        TotalTask = 2
        workflow = {i:Task(i, runtime=random.randint(MINDATA,MAXDATA)) for i in range(TotalTask)}
        nb_tasks = [1,1]  # 每层任务的个数
        nb_tasks0 = [0,0]    
        k = 0
        i = 0
        while k<TotalTask:
            if nb_tasks0[i]<nb_tasks[i]:
                workflow[k].name = i
                k += 1
                nb_tasks0[i] += 1
            else:
                i += 1
        for i,j in edge:
            size_temp = random.randint(MINDATA/100,MAXDATA/1000)
            child = File(j,id=j,size = size_temp,booleanoutput=True)
            workflow[i].outputs.append(child)

            parent = File(i,id=i,size = size_temp,booleaninput=True)
            workflow[j].inputs.append(parent)
        PFactor = [1,0]
        for i in range(len(workflow)):            
            workflow[i].MI = PFactor[i]
        # MET = getMET(workflow)
        # EST,EFT = getEST(workflow,MET)
        # Deadline = max(EFT)
        # DeadlineFactor = 1.1
        # workflow['Deadline'] = math.trunc(Deadline*DeadlineFactor)
        # workflow['DeadlineFactor'] = DeadlineFactor

        # drawDAG(workflow,nb_tasks)

        return workflow

    def RandomDAG_L3():
        edge = [(0,2),(1,2),(2,3)]
        TotalTask = 4
        workflow = {i:Task(i, runtime=random.randint(MINDATA,MAXDATA)) for i in range(TotalTask)}
        nb_tasks = [2,1,1]  # 每层任务的个数
        nb_tasks0 = [0,0,0]    
        k = 0
        i = 0
        while k<TotalTask:
            if nb_tasks0[i]<nb_tasks[i]:
                workflow[k].name = i
                k += 1
                nb_tasks0[i] += 1
            else:
                i += 1
        for i,j in edge:
            size_temp = random.randint(MINDATA/100,MAXDATA/1000)
            child = File(j,id=j,size = size_temp,booleanoutput=True)
            workflow[i].outputs.append(child)

            parent = File(i,id=i,size = size_temp,booleaninput=True)
            workflow[j].inputs.append(parent)
        PFactor = [1,0,1,0]
        for i in range(len(workflow)):            
            workflow[i].MI = PFactor[i]
        # MET = getMET(workflow)
        # EST,EFT = getEST(workflow,MET)
        # Deadline = max(EFT)
        # DeadlineFactor = 1.1
        # workflow['Deadline'] = math.trunc(Deadline*DeadlineFactor)
        # workflow['DeadlineFactor'] = DeadlineFactor

        # drawDAG(workflow,nb_tasks)

        return workflow
    
    def RandomDAG_L4():
        edge = [(0,1),(0,2),(0,3),
                (1,4),(2,4),(3,5),                
                (4,6),(5,6)]
        TotalTask = 7
        workflow = {i:Task(i, runtime=random.randint(MINDATA,MAXDATA)) for i in range(TotalTask)}
        nb_tasks = [1,3,2,1]  # 每层任务的个数
        nb_tasks0 = [0,0,0,0]    
        k = 0
        i = 0
        while k<TotalTask:
            if nb_tasks0[i]<nb_tasks[i]:
                workflow[k].name = i
                k += 1
                nb_tasks0[i] += 1
            else:
                i += 1
        for i,j in edge:
            size_temp = random.randint(MINDATA/100,MAXDATA/1000)
            child = File(j,id=j,size = size_temp,booleanoutput=True)
            workflow[i].outputs.append(child)

            parent = File(i,id=i,size = size_temp,booleaninput=True)
            workflow[j].inputs.append(parent)
        PFactor = [1,0,1,0,0,0,0]
        for i in range(len(workflow)):            
            workflow[i].MI = PFactor[i]
        # MET = getMET(workflow)
        # EST,EFT = getEST(workflow,MET)
        # Deadline = max(EFT)
        # DeadlineFactor = 1.1
        # workflow['Deadline'] = math.trunc(Deadline*DeadlineFactor)
        # workflow['DeadlineFactor'] = DeadlineFactor

        # drawDAG(workflow,nb_tasks)

        return workflow



def generateTasks(workflow):
    ###################
    # 计算DAG的深度和宽度
    # 计算DAG的深度 nb_levels
    # 每层任务的个数 nb_tasks[i]
    # 任务所在的层数 nb_level_task[i]    
    # #############
    list1 = math.modf(math.exp(ALPHA * math.log(NUM_TASKS)))
    nb_tasks_per_level = int(list1[1])     
    total_nb_tasks = 0
    nb_tasks = []
    widthFactors = int(math.sqrt(NUM_TASKS)*ALPHA)
    while 1:
        # tmp = getIntRandomNumberAround(nb_tasks_per_level, 100.00 - 100.0*ALPHA)
        tmp = random.randint(1,2*widthFactors)
        if (total_nb_tasks + tmp > NUM_TASKS):
            tmp = NUM_TASKS - total_nb_tasks
        
        nb_tasks.append(tmp) 
        total_nb_tasks += tmp
        if (total_nb_tasks >= NUM_TASKS):
            break       

    nb_levels = len(nb_tasks)   #height (depth) of a DAG
    nb_level_task = []
    tasks_per_level = []
    k = 0
    for i in range(nb_levels):
        tasks_per_level.insert(len(tasks_per_level),[])
        for j in range(nb_tasks[i]):    
            workflow[k].name = i   # name存的是level
            tasks_per_level[i].append(k)
            k += 1
            nb_level_task.append(i)

    return tasks_per_level,nb_tasks,nb_level_task

def generateDependencies(workflow,tasks_per_level):
    '''
    生成DAG的边：1.确定父节点的个数；2.确定每个父节点所在的层；3.确定具体哪个节点
    '''
    # for 
    for i in range(1,len(tasks_per_level)):
        for each_task in tasks_per_level[i]:
            nb_parents = min(1 + int(DENSITY*len(tasks_per_level[i-1])*random.random()) ,len(tasks_per_level[i-1]))
            list_parents = []
            for k in range(nb_parents):
                while 1:
                    # /* compute the level of the parent */
                    parent_level = max(0, i- random.randint(1,JUMP))
                    # /* compute which parent */
                    parent_index = random.randint(0,len(tasks_per_level[parent_level])-1)
                    if not (tasks_per_level[parent_level][parent_index] in list_parents) : break
                list_parents.append(tasks_per_level[parent_level][parent_index])
                parent = File(tasks_per_level[parent_level][parent_index],
                                id=tasks_per_level[parent_level][parent_index],
                                size = random.randint(MINDATA/100,MAXDATA/100),
                                booleaninput=True)
                
                workflow[each_task].inputs.append(parent)
                # workflow[each_task].inputs[len(workflow[each_task].inputs)-1].booleaninput = True

                child = File(each_task,id=each_task,size = parent.size,booleanoutput=True)
                workflow[tasks_per_level[parent_level][parent_index]].outputs.append(child)

def getMET(workflow):
    MET = [0 for each in range(len(workflow))]  # {}#
    for taskid,task in workflow.items():
        MET[taskid] =task.runtime /GlobalResource.minECU #math.trunc( )   
    return MET

def breadth_first_search(workflow):#从前往后
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

def getEST(workflow,MET):
    scheduleOrder = breadth_first_search(workflow)
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
                listPEST = [ EST[each.id] + MET[each.id] + each.size/GlobalResource.minB for each in parents  ] #
                EST[taskid] = max(listPEST)
            else:
                EST[taskid] = 0
            EFT[taskid] = EST[taskid] + MET[taskid]
            scheduleOrder.remove(taskid)
            break
    return EST,EFT

def drawDAG(workflow,nb_tasks):
    ## 先计算位置 任务最多的层的任务数   task.name暂时保存的是所在的层数
    max_num_task_level = max(nb_tasks)
    list_i = [1 for i in range(len(nb_tasks))]

    G = nx.DiGraph()
    for i in range(len(workflow)-2):
        G.add_node(i )   #,desc= '$T_{'+str(i)+'}$' 
    pos = []    
    node_colors = []
    # colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf','#1a55FF']    
    colors = ['red', 'orange', 'gold', 'lawngreen', 'lightseagreen', 'royalblue','blueviolet']
    options = {"with_labels": True, "node_color": "white", "edgecolors": "black"}
    marks = ["","\\","/","+",".","*"] # ,"X" ,"o"
    for id,task in workflow.items():
        if str(id).isnumeric() :
            for j in task.outputs:
                G.add_edge(id,j.id) # ,name=str(j.size)
            # '''
            # MolecularDynamicsCode  绘图
            if id >=11 and id <=12:
                pos.append((task.name, 
                (max_num_task_level-nb_tasks[task.name]+2*list_i[task.name]-1)/2-0.25*(13-id) ) )
            elif id >=13 and id <=14:
                pos.append((task.name, 
                (max_num_task_level-nb_tasks[task.name]+2*list_i[task.name]-1)/2+0.5*(id-12) ))
            elif id >=15 and id <=20:
                pos.append((task.name, 
                (max_num_task_level-nb_tasks[task.name]+2*list_i[task.name]-1)/2-0.25*(id-14) ) )
            elif id ==21:
                pos.append((task.name, 
                (max_num_task_level-nb_tasks[task.name]+2*list_i[task.name]-1)/2-0.25  ))
            elif id >=22 and id <=26:
                pos.append((task.name, 
                (max_num_task_level-nb_tasks[task.name]+2*list_i[task.name]-1)/2-0.25*(id-21) ) )
            else:
                pos.append((task.name, 
                (max_num_task_level-nb_tasks[task.name]+2*list_i[task.name]-1)/2+0.25*(random.random()-random.random())  ))
            # '''
            # 加减0.25 调整
            # pos.append((task.name+0.25*(random.random()-random.random()), (max_num_task_level-nb_tasks[task.name]+2*list_i[task.name]-1)/2+0.25*(random.random()-random.random())  ))
            # 不调整
            # pos.append((task.name, (max_num_task_level-nb_tasks[task.name]+2*list_i[task.name]-1)/2))
            list_i[task.name] += 1
            node_colors.append(colors[ task.name%len(colors)])  
    node_labels = nx.get_node_attributes(G, 'desc') # 画出标签
    nx.draw(G, pos, labels=node_labels,width= 0.25,node_size=100, **options) # 加颜色 ,node_color=node_colors  
    # edge_labels = nx.get_edge_attributes(G, 'name')# 画出边权值
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # plt.title('DAG', fontsize=10)
    plt.show()



def ResetDeadline(workflow,DeadlineFactor):    
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
    
    MET = getMET_SubDeadline(workflow)          #  /GlobalResource.maxECU
    EST,EFT = getEST_SubDeadline(workflow,MET)  #  /GlobalResource.maxB
    Deadline = max(EFT)*DeadlineFactor
    return Deadline


workflowL2 = RandomlyGeneratedApplicationGraphs.RandomDAG_L2()
workflowL3 = RandomlyGeneratedApplicationGraphs.RandomDAG_L3()
workflowL4 = RandomlyGeneratedApplicationGraphs.RandomDAG_L4()
multiWorflow = [workflowL2,workflowL3,workflowL4]
for i in range(3):    
    DeadlineFactor = 1.1 
    Deadline = ResetDeadline(multiWorflow[i],DeadlineFactor)
    multiWorflow[i]['Deadline'] = math.trunc(Deadline*DeadlineFactor)
    multiWorflow[i]['DeadlineFactor'] = DeadlineFactor
currentpath = os.getcwd()
np.save(currentpath+'\\'+'test_multiWorflow.npy', multiWorflow)



NUM_TASKS = 6 # 10          # Number of tasks in the graph, (v)

# workflow = RandomlyGeneratedApplicationGraphs.generateWorkflow()
# workflow = RandomlyGeneratedApplicationGraphs.GeneratedGaussianEliminationAlgorithm()
# workflow = RandomlyGeneratedApplicationGraphs.MolecularDynamicsCode()
# NUM_TASKS = 6 # 10 

# ####################  生成数据 并将字典格式的workflow存到 .npy文件    ####################################
# global NUM_TASKS
# listDeadlineFactor = [0.8,1.1,1.5,1.8] 

# listfileName = [i for i in range(5,51,5)]  # GaussianEliminationAlgorithm_
# for NUM_TASKS in listfileName:  
#     TatalTaskNum = int((NUM_TASKS*NUM_TASKS+NUM_TASKS-2)/2)
#     fileName  = 'GaussianElimination_'+str(NUM_TASKS)+'_'+str(TatalTaskNum)
#     print('****************\t\t\t' + str(fileName) + ' is running. \t\t\t****************')
#     workflow = RandomlyGeneratedApplicationGraphs.GeneratedGaussianEliminationAlgorithm()

# # listfileName = [i for i in range(10)]  
# # for NUM_TASKS in listfileName:  #   此处的NUM_TASKS 用来生成问题的个数
# #     fileName  = 'MolecularDynamicsCode_41_'+str(NUM_TASKS)
# #     print('****************\t\t\t' + str(fileName) + ' is running. \t\t\t****************')
# #     workflow = RandomlyGeneratedApplicationGraphs.MolecularDynamicsCode()

#     MET = getMET(workflow)
#     EST,EFT = getEST(workflow,MET)
#     Deadline = max(EFT)
#     for DeadlineFactor in listDeadlineFactor:
#         workflow['Deadline'] = math.trunc(Deadline*DeadlineFactor)
#         workflow['DeadlineFactor'] = DeadlineFactor
#         currentpath = os.getcwd()
#         np.save(currentpath+'\\data_npy\\'+fileName+'.xml_'+str(DeadlineFactor)+'.npy', workflow)                  #保存字典 注意带上后缀名
# k = 1
# ###############################################################################################



# k= 1