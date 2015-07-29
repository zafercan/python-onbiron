#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from serverFacade import ServerFacade

class MqttClient(object):
    server = None
    
    def __init__(self, name): 
        client = mqtt.Client()
        self.name = name
        server = ServerFacade.getInstance()
        client.on_connect = self.on_connect.__func__
        client.on_message = self.on_message.__func__
        client.on_subscribe = self.on_subscribe.__func__
        client.on_publish = self.on_publish.__func__
        
        client.connect(server.brokerIp, 1903, 60)
        client.loop_forever()
        
    
    def on_connect(client, userdata, rc):
        print 'Connected with result code ' + str(rc)
        client.subscribe(ServerFacade.getInstance().PARAM_REGID)
    
    def on_message(client, userdata, msg):
        print msg.topic + '----' + str(msg.payload)
        ServerFacade.getInstance().initMonitoring()
        # ServerFacade.getInstance().getNotification()
        # message = "PUBLISH TEST !!!!	"
        # client.publish('$SYS/broker/version', message)

    def on_publish(mqttc, obj, mid):
        print 'PUBLISHED! ' + str(mid)

    def on_subscribe(mqttc, obj, mid, granted_qos):
        print 'SUBSCRIBED! - ' + str(mid) + ' ' + str(granted_qos)


