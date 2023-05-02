class VMScheduling:
    def __init__(self,id = None,NumCores=0,TaskCore=[],VMTime=[],CompleteTime=[],):#TaskTime=[],
        '''
        VM号、任务所在的核（列表的长度为核数）、任务的开始、结束时间
        
        '''       
        self.id = id #VM类型号，对应VMType
        self.NumCores = NumCores #VM的核数
        self.TaskCore = [[] for i in range(self.NumCores)]  #核上执行的任务序列
        self.VMTime = [[] for i in range(self.NumCores)]    #核上执行任务时的开始时间、结束时间
        # self.TaskTime = TaskTime                            #
        self.CompleteTime = [0 for i in range(self.NumCores)] #核的当前完成时间
    
    # def __repr__(self):
    #     return self.name#"<File %s>" % 