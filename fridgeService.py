#!/usr/bin/python
# -*- coding: utf-8 -*-

# import mqttClient

from mqttClient import MqttClient
from serverFacade import ServerFacade

 
serverFacade = ServerFacade.getInstance()
#serverFacade.getClientKey()
#serverFacade.getToken()
#serverFacade.getSenderId()
#serverFacade.getLicense()
#if serverFacade.getRegister() == True:
#    if serverFacade.getIsRegistered() == True:
mqttc = MqttClient('client1')
serverFacade.initMonitoring()       
#serverFacade.Unregister()


