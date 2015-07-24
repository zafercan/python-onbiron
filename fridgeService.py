#!/usr/bin/python
# -*- coding: utf-8 -*-

# import mqttClient

from mqttClient import MqttClient
from serverFacade import ServerFacade

# mqttc = MqttClient('client1')

serverFacade = ServerFacade()
serverFacade.getClientKey()
serverFacade.getToken()

 # print result
