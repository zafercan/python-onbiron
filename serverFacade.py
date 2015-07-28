#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import httplib
import json
import base64
from decorator import Singleton


# get - post operations
@Singleton
class ServerFacade(object):

    # members

    clientKey = ''
    clientSecret = ''
    accessToken = ''
    brokerIp = ''
    brokerPort = ''
    jsonData = ''
    featureCodes = ''
    # server parameters

    SERVER_IP = ''
    PORT = '9763'

    # web service api

    BASE_URL = SERVER_IP + ':' + PORT
    API_CLIENT_KEY = '/emm/api/devices/clientkey'
    API_TOKEN = '/oauth2/token'
    API_SENDER_ID = '/emm/api/devices/sender_id/1.0.0?domain='
    API_LICENSE = '/emm/api/devices/license/1.0.0?domain='
    API_REGISTER = '/emm/api/devices/register/1.0.0'
    API_ISREGISTERED = '/emm/api/devices/isregistered/1.0.0'
    API_UNREGISTER = '/emm/api/devices/unregister/1.0.0'
    API_NOTIFICATION = '/emm/api/notifications/pendingOperations/1.0.0'

    # parameters

    PARAM_USERNAME = ''
    PARAM_PASSWORD = ''
    DEFAULT_POST_HEADER = \
        {'Content-type': 'application/x-www-form-urlencoded',
         'Authorization': ''}
    DEFAULT_VALUES = {'username': PARAM_USERNAME,
                      'password': PARAM_PASSWORD}

    PARAM_PLATFORM = 'Android'
    PARAM_USER_AGENT = 'Linux Android'
    PARAM_REGID = 'abcdefgh12345678'
    PARAM_PROPERTIES = \
        '{"device":"fridge","imei":"1234567890abcde","imsi":"310260000000000","model":"Grundig Fridge","fw_ver":2.3,"agent_ver":1}'
    PARAM_VENDOR = 'Grundig'
    PARAM_MAC = '08:00:27:66:fa:d4'
    PARAM_TYPE = 'BYOD'
    PARAM_OSVERSION = '2.3'

    # URL_CLIENT_KEY = BASE_URL + API_CLIENT_KEY
    # URL_TOKEN = BASE_URL + API_TOKEN
    
    def __init__(self):
        self.brokerIp = 'brokerer'
        
        with open('json/featureCodes.json') as data_file:    
            self.featureCodes = json.load(data_file)    
        
    def postResponse(self, api, method):
        data = urllib.urlencode(self.DEFAULT_VALUES)
        h = httplib.HTTPConnection(self.BASE_URL)
        h.request(method, api, data, self.DEFAULT_POST_HEADER)
        response = h.getresponse()
        read = response.read()
        print read + '\n'

        try:
            json_object = json.loads(read)
        except ValueError, e:
            return read
        return json_object

        # return read

    def generateBasicAuthorizationString(self):
        title = 'Basic '
        data = self.clientKey + ':' + self.clientSecret
        encodedData = base64.b64encode(data)
        string = title + encodedData
        return string

    def generateBearerAuthorizationString(self):
        title = 'Bearer '
        data = self.accessToken
        string = title + data
        return string

    def getClientKey(self):

        api = self.API_CLIENT_KEY
        method = 'POST'
        j = self.postResponse(api, method)
        self.clientKey = j['clientkey']
        self.clientSecret = j['clientsecret']
        self.brokerIp = j['brokerip']
        self.brokerPort = j['brokerport']

    def getToken(self):

        api = self.API_TOKEN
        method = 'POST'
        self.DEFAULT_VALUES['grant_type'] = 'password'
        base64EncodedData = self.generateBasicAuthorizationString()
        self.DEFAULT_POST_HEADER['Authorization'] = base64EncodedData

        j = self.postResponse(api, method)
        self.accessToken = j['access_token']

    def getSenderId(self):
        api = self.API_SENDER_ID
        method = 'GET'
        self.DEFAULT_POST_HEADER['Authorization'] = \
            self.generateBearerAuthorizationString()
        self.postResponse(api, method)

    def getLicense(self):
        api = self.API_LICENSE
        method = 'GET'
        self.DEFAULT_POST_HEADER['Authorization'] = \
            self.generateBearerAuthorizationString()
        return self.postResponse(api, method)

    def getRegister(self):
        api = self.API_REGISTER
        method = 'POST'
        self.DEFAULT_VALUES['platform'] = self.PARAM_PLATFORM
        self.DEFAULT_VALUES['regid'] = self.PARAM_REGID
        self.DEFAULT_VALUES['properties'] = self.PARAM_PROPERTIES
        self.DEFAULT_VALUES['username'] = self.PARAM_USERNAME
        self.DEFAULT_VALUES['vendor'] = self.PARAM_VENDOR
        self.DEFAULT_VALUES['mac'] = self.PARAM_MAC
        self.DEFAULT_VALUES['type'] = self.PARAM_TYPE
        self.DEFAULT_VALUES['osversion'] = self.PARAM_OSVERSION
        self.DEFAULT_POST_HEADER['Authorization'] = \
            self.generateBearerAuthorizationString()
        self.DEFAULT_POST_HEADER['User-Agent'] = self.PARAM_USER_AGENT

        if self.postResponse(api, method) == 'registered':
            return True
        else:
            return False

    def getIsRegistered(self):
        api = self.API_ISREGISTERED
        method = 'POST'
        self.DEFAULT_VALUES['regid'] = self.PARAM_REGID
        self.DEFAULT_POST_HEADER['Authorization'] = \
            self.generateBearerAuthorizationString()

        if self.postResponse(api, method) == 'registered':
            return True
        else:
            return False

    def Unregister(self):
        api = self.API_UNREGISTER
        method = 'POST'
        self.DEFAULT_POST_HEADER['Authorization'] = \
            self.generateBearerAuthorizationString()
        self.DEFAULT_VALUES['regid'] = self.PARAM_REGID
        return self.postResponse(api, method)

    def getPendingNotifications(self):
        api = self.API_NOTIFICATION
        method = 'POST'
        self.DEFAULT_POST_HEADER['Authorization'] = \
            self.generateBearerAuthorizationString()
        self.DEFAULT_VALUES['regId'] = self.PARAM_REGID

        # self.DEFAULT_VALUES['data'] = ''
        k = self.postResponse(api, method)
        
        return k
        
    def sendPendingNotifications(self, json_data):
        api = self.API_NOTIFICATION
        method = 'POST'
        self.DEFAULT_POST_HEADER['Authorization'] = \
            self.generateBearerAuthorizationString()
        self.DEFAULT_VALUES['regId'] = self.PARAM_REGID
        self.DEFAULT_VALUES['data'] = json_data
        self.postResponse(api, method)
        
    def doOperation(self, datas):
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
        notifications["regId"] = self.PARAM_REGID
        notifications["data"] = datas
        #json.dumps(notifications)
        print 'NOTIFICATIONS :: '
        print notifications
        #json_data = json.dumps(notifications)

        return json.dumps(notifications)
    
    def initMonitoring(self):
        datas = self.getPendingNotifications() 
        print 'DATAS : '
        print datas
        if datas != None:
             
            json_data = self.doOperation(datas)
            #send response to the server
            self.sendPendingNotifications(json_data)
        