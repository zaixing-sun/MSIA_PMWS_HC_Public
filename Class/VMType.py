
class PrivateCloudVMType(object):
    def __init__(self):#, m,P, N, U,B,M

        self.m      = 3  # int(m) # 
        self.P      = [i for i in range(self.m)]
        # self.N      = [1,       2,      4,      8,      16,     32]   #
        self.N      = [1,       1,      1]
        self.B      = [1.25,    1.75,   2.5]          #
        self.ECU    = [10,      15,     22] 
        self.M      = [0,       0,      0]      #
        self.ProcessingCapacity = [4.4*i for i in self.ECU ]        #
        self.price_ProCap = [self.M[i]/self.ProcessingCapacity[i] for i in self.P]
        self.dynamic_power = [110,    190,  300] # 
        self.idle_power = [10,    20,   35]
        self.trans_power = 5

class VMType(object):
    def __init__(self):#, m,P, N, U,B,M
        self.m      = 5  # int(m) # 
        self.P      = [i for i in range(self.m)]
        # self.N      = [1,       2,      4,      8,      16,     32]  #  [1,2,4,8,16]
        self.N      = [1,       1,      1,      1,      1]
        self.B      = [1,       1.5,    2,      3,      3]                 
        self.ECU    = [7,       14,     28,     55,     108] 
        self.M      = [0.128,   0.255,  0.511,  1.021,  2.043]  #
        self.ProcessingCapacity = [4.4*i for i in self.ECU ]  #
        self.price_ProCap = [self.M[i]/self.ProcessingCapacity[i] for i in range(self.m)]
        self.price_trans_data = {'IN':0.09,'OUT':0.02}#[0.09, 0.02] 
        self.price_store_data = 0.1056  #

