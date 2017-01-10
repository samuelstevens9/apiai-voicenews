import os,json

class AISessions(object):
    
    sessionID = None
    sessionData = {}
    
    def __init__(self,sessionID,dir_name="apiai_sessions"):
        self.sessionID = sessionID
        if(not os.path.isdir(dir_name)):
            os.mkdir(dir_name)
        
        with open(self.sessionID+'.json') as data_file:    
            self.sessionData = json.load(data_file)
    
    def save(self):
        with open(self.sessionID+'.json', 'w') as outfile:
            json.dump(self.sessionData, outfile)
    