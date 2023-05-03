class VMScheduling:
    def __init__(self,id = None,NumCores=0,TaskCore=[],VMTime=[],CompleteTime=[],):#TaskTime=[],
        self.id = id 
        self.NumCores = NumCores
        self.TaskCore = [[] for i in range(self.NumCores)]  
        self.VMTime = [[] for i in range(self.NumCores)]    
        self.CompleteTime = [0 for i in range(self.NumCores)] 