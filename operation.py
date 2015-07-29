import json

class Operation(object):
    
    featureCodes = ''
    
    def __init__(self):
        with open('json/featureCodes.json') as data_file:    
            self.featureCodes = json.load(data_file)    
             
    def doOperation(self, datas,regid):
        
        #for each feature code do the task
        for index in range(len(datas)):
            print 'INCOME : ' 
            print datas[index]['code']
            if datas[index]['code'] == self.featureCodes['CODES']['APPLIST']:
                datas[index]['data'][0]['data'] = json.loads('[{"data":[{"package":"com.onbiron.mdm.agent","icon":"","name":"WSO2 Agent"},{"package":"com.example.android.apis","icon":"","name":"API Demos"},{"package":"com.android.gesture.builder","icon":"","name":"Gesture Builder"}],"status":"true","code":"502A"}]')
            elif datas[index]['code'] == self.featureCodes['CODES']['INFO']:     
                datas[index]['data'][0]['data'] = json.loads('[{"data":{"internal_memory":{"total":4.84,"available":4.75},"location_obj":{"longitude":32.7758713,"latitude":39.898896},"operator":["Android"],"external_memory":{"total":4.84,"available":4.75},"battery":{"level":88}},"status":"true","code":"500A"}]')
        #json.dumps(datas)
        notifications = {}
        notifications["regId"] = regid
        notifications["data"] = datas
        #json.dumps(notifications)
        print 'NOTIFICATIONS :'
        print notifications
        #json_data = json.dumps(notifications)

        return json.dumps(notifications)