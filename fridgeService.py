#!/usr/bin/python
# -*- coding: utf-8 -*-

# import mqttClient

from mqttClient import MqttClient
from serverFacade import ServerFacade

 
serverFacade = ServerFacade.getInstance()
serverFacade.initiateRegistration()

if serverFacade.registerDevice() == True:
    if serverFacade.isRegistered() == True:
        mqttc = MqttClient('client1')
        serverFacade.initMonitoring()   
    else:
        serverFacade.initiateRegistration()
        serverFacade.registerDevice()
else:
    serverFacade.unregister()
    serverFacade.initiateRegistration()
    serverFacade.registerDevice()
    mqttc = MqttClient('client1')
    serverFacade.initMonitoring()
    
    


