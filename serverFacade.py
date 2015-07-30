#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import httplib
import json
import base64
from decorator import Singleton
from operation import Operation
from systemInfo import SystemInfo

# get - post operations
@Singleton
class ServerFacade(object):

    # members
        
    clientKey = ''
    clientSecret = ''
    accessToken = ''
    brokerIp = ''
    brokerPort = '' 
    operation = None
    mac = ''
    configs = ''
    
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
    
    #load config file
    with open('json/config.json') as config_file:    
        configs = json.load(config_file) 
    
    system = SystemInfo()
    
    # update config file
    configs['CONFIG']['PARAM_REGID'] = system.getRegId()
    configs["CONFIG"]["PARAM_OSVERSION"] = system.getOsVersion()
    configs['CONFIG']['PARAM_MAC'] = system.getWlanMac()
    configs['CONFIG']['DEFAULT_VALUES']['username'] = configs['CONFIG']['PARAM_USERNAME']
    configs['CONFIG']['DEFAULT_VALUES']['password'] = configs['CONFIG']['PARAM_PASSWORD']
    configs['CONFIG']['PARAM_PROPERTIES']['fw_ver'] = system.getFWVersion()
    
    configs['FEATURE_DATA']['APPLIST'][0]['data']['storage']['total'] = system.getTotalDiskSpace()
    configs['FEATURE_DATA']['APPLIST'][0]['data']['storage']['available'] = system.getFreeDiskSpace()
    configs['FEATURE_DATA']['APPLIST'][0]['data']['agent']['cpu'] = system.getCpuUsage()
    configs['FEATURE_DATA']['APPLIST'][0]['data']['agent']['memory'] = system.getTotalRam()
    
    location = system.getLocation()
    configs['FEATURE_DATA']['APPLIST'][0]['data']['location_obj']['longitude'] = location['longitude']
    configs['FEATURE_DATA']['APPLIST'][0]['data']['location_obj']['latitude'] = location['latitude']
    
    # parameters
    
    PARAM_USERNAME = configs['CONFIG']['DEFAULT_VALUES']['username']
    PARAM_PASSWORD = configs['CONFIG']['DEFAULT_VALUES']['password']
    DEFAULT_POST_HEADER = configs['CONFIG']['DEFAULT_POST_HEADER']
    DEFAULT_VALUES = configs['CONFIG']['DEFAULT_VALUES']
    PARAM_PLATFORM = configs['CONFIG']['PARAM_PLATFORM']
    PARAM_USER_AGENT = configs['CONFIG']['PARAM_USER_AGENT']
    PARAM_REGID = str(configs['CONFIG']['PARAM_REGID'])
    PARAM_PROPERTIES = configs['CONFIG']['PARAM_PROPERTIES']
    PARAM_VENDOR = configs['CONFIG']['PARAM_VENDOR']
    PARAM_MAC = configs['CONFIG']['PARAM_MAC']
    PARAM_TYPE = configs['CONFIG']['PARAM_TYPE']
    PARAM_OSVERSION = configs['CONFIG']['PARAM_OSVERSION']
    
    def __init__(self):
        self.operation = Operation()
        
    def initiateRegistration(self):
        self.getClientKey()
        self.getToken()
        self.getSenderId()
        self.getLicense()
        
    def postResponse(self, api, method):
        data = urllib.urlencode(self.DEFAULT_VALUES)
        h = httplib.HTTPConnection(self.BASE_URL)
        h.request(method, api, data, self.DEFAULT_POST_HEADER)
        response = h.getresponse()
        read = response.read()
        print read + '\n'

        try:
            responseJsonObject = json.loads(read)
        except ValueError, e:
            return read
        return responseJsonObject

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
        self.DEFAULT_POST_HEADER['Authorization'] = self.generateBearerAuthorizationString()
        self.postResponse(api, method)

    def getLicense(self):
        api = self.API_LICENSE
        method = 'GET'
        self.DEFAULT_POST_HEADER['Authorization'] = self.generateBearerAuthorizationString()
        return self.postResponse(api, method)

    def registerDevice(self):
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
        self.DEFAULT_POST_HEADER['Authorization'] = self.generateBearerAuthorizationString()
        self.DEFAULT_POST_HEADER['User-Agent'] = self.PARAM_USER_AGENT

        if self.postResponse(api, method) == 'registered':
            return True
        else:
            return False

    def isRegistered(self):
        api = self.API_ISREGISTERED
        method = 'POST'
        self.DEFAULT_VALUES['regid'] = self.PARAM_REGID
        self.DEFAULT_POST_HEADER['Authorization'] = self.generateBearerAuthorizationString()

        if self.postResponse(api, method) == 'registered':
            return True
        else:
            return False

    def unregister(self):
        api = self.API_UNREGISTER
        method = 'POST'
        self.DEFAULT_POST_HEADER['Authorization'] = self.generateBearerAuthorizationString()
        self.DEFAULT_VALUES['regid'] = self.PARAM_REGID
        return self.postResponse(api, method)

    def getPendingNotifications(self):
        api = self.API_NOTIFICATION
        method = 'POST'
        self.DEFAULT_POST_HEADER['Authorization'] = self.generateBearerAuthorizationString()
        self.DEFAULT_VALUES['regId'] = self.PARAM_REGID
        return self.postResponse(api, method)
         
    def sendPendingNotifications(self, notificationData):
        api = self.API_NOTIFICATION
        method = 'POST'
        self.DEFAULT_POST_HEADER['Authorization'] = self.generateBearerAuthorizationString()
        self.DEFAULT_VALUES['regId'] = self.PARAM_REGID
        self.DEFAULT_VALUES['data'] = notificationData
        self.postResponse(api, method)
            
    def initMonitoring(self):
        datas = self.getPendingNotifications() 
        print 'DATAS : '
        print datas
        if datas != None:
            notificationData = self.operation.doOperation(datas, self.PARAM_REGID)
            #send response to the server
            self.sendPendingNotifications(notificationData)
        