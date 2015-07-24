#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt


class MqttClient(object):

    def __init__(self, name):
        print 'init'
        client = mqtt.Client()
        self.name = name
        client.on_connect = self.on_connect.__func__
        client.on_message = self.on_message.__func__
        client.on_subscribe = self.on_subscribe.__func__
        client.on_publish = self.on_publish.__func__
        client.connect('test.mosquitto.org', 1883, 60)
        client.loop_forever()

    def on_connect(client, userdata, rc):
        print 'Connected with result code ' + str(rc)
        client.subscribe('$SYS/broker/version')

    def on_message(client, userdata, msg):
        print msg.topic + '----' + str(msg.payload)
        message = "PUBLISH TEST !!!!	"
        client.publish('$SYS/broker/version', message)

    def on_publish(mqttc, obj, mid):
        print 'PUBLISHED! ' + str(mid)

    def on_subscribe(
        mqttc,
        obj,
        mid,
        granted_qos,
        ):

        print 'SUBSCRIBED! - ' + str(mid) + ' ' + str(granted_qos)


