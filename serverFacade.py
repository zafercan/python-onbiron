#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import httplib
import json
import base64


# get - post operations

class ServerFacade(object):

    # members

    clientKey = ''
    clientSecret = ''
    accessToken = ''

    # server parameters

    SERVER_IP = '193.140.63.159'
    PORT = '9763'

    # web service api

    BASE_URL = SERVER_IP + ':' + PORT
    API_CLIENT_KEY = '/emm/api/devices/clientkey'
    API_TOKEN = '/oauth2/token'
    API_REGISTER = '/emm/api/devices/register/1.0.0'

    # parameters

    PARAM_USERNAME = 'test-onbiron'
    PARAM_PASSWORD = 'test-onbiron'
    DEFAULT_POST_HEADER = \
        {'Content-type': 'application/x-www-form-urlencoded',
         'Authorization': ''}
    DEFAULT_VALUES = {'username': PARAM_USERNAME,
                      'password': PARAM_PASSWORD,
                      'grant_type': 'password'}

    # URL_CLIENT_KEY = BASE_URL + API_CLIENT_KEY
    # URL_TOKEN = BASE_URL + API_TOKEN

    def postResponse(self, api, method):
        data = urllib.urlencode(self.DEFAULT_VALUES)
        h = httplib.HTTPConnection(self.BASE_URL)
        h.request(method, api, data, self.DEFAULT_POST_HEADER)
        response = h.getresponse()
        read = response.read()
        print read
        j = json.loads(read)
        return j

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

        # print self.clientKey + '--' + self.clientSecret

    def getToken(self):

        api = self.API_TOKEN
        method = 'POST'
        base64EncodedData = self.generateBasicAuthorizationString()
        self.DEFAULT_POST_HEADER['Authorization'] = base64EncodedData

        j = self.postResponse(api, method)
        self.accessToken = j['access_token']

        print self.accessToken

    def getSenderId(self):
        api = '/emm/api/devices/sender_id/1.0.0?domain='
        method = 'GET'
        self.DEFAULT_POST_HEADER['Authorization'] = \
            self.generateBearerAuthorizationString()
        self.postResponse(api, method)


