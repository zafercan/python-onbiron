import json
 
class Operation(object):
    
    featureCodes = ''
    configs = ''
    
    def __init__(self):
        with open('json/featureCodes.json') as data_file:    
            self.featureCodes = json.load(data_file)    
        
        with open('json/config.json') as config_file:    
            self.configs = json.load(config_file)
             
    def doOperation(self, datas,regid):
        
        #for each feature code do the task
        for index in range(len(datas)):
            print 'INCOME : ' 
            print datas[index]['code']
            if datas[index]['code'] == self.featureCodes['CODES']['APPLIST']:
                datas[index]['data'][0]['data'] = json.loads(self.configs['FEATURE_DATA']['APPLIST'])
            elif datas[index]['code'] == self.featureCodes['CODES']['INFO']:     
                datas[index]['data'][0]['data'] = json.loads(self.configs['FEATURE_DATA']['INFO'])
        #json.dumps(datas)
        notifications = {}
        notifications["regId"] = regid
        notifications["data"] = datas
        #json.dumps(notifications)
        print 'NOTIFICATIONS :'
        print notifications
        #json_data = json.dumps(notifications)

        return json.dumps(notifications)