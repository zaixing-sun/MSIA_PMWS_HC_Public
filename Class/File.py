'''
Created on 15-Mar-2017

@author: itadmin
'''
class File:
    def __init__(self, name,id = None, size=0,booleaninput=False, booleanoutput=False):#
        self.name = name        
        self.size = size
        self.id = id
        self.booleaninput = booleaninput
        self.booleanoutput = booleanoutput
    
    def __repr__(self):
        return self.name#"<File %s>" % 

    def changeID(self,id):
        self.id = id 