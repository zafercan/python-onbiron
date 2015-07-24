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

    SERVER_IP = ''
    PORT = '9763'

    # web service api

    BASE_URL = SERVER_IP + ':' + PORT
    API_CLIENT_KEY = '/emm/api/devices/clientkey'
    API_TOKEN = '/oauth2/token'

    # parameters

    PARAM_USERNAME = ''
    PARAM_PASSWORD = ''
    DEFAULT_POST_HEADER = \
        {'Content-type': 'application/x-www-form-urlencoded',
         'Authorization': ''}
    DEFAULT_VALUES = {'username': PARAM_USERNAME,
                      'password': PARAM_PASSWORD,
                      'grant_type': 'password'}

    # URL_CLIENT_KEY = BASE_URL + API_CLIENT_KEY
    # URL_TOKEN = BASE_URL + API_TOKEN

    def postResponse(self, api):
        data = urllib.urlencode(self.DEFAULT_VALUES)
        h = httplib.HTTPConnection(self.BASE_URL)
        h.request('POST', api, data, self.DEFAULT_POST_HEADER)
        response = h.getresponse()
        read = response.read()

        j = json.loads(read)
        return j

        # return read

    def generateBasicAuthorizationString(self):
        title = 'Basic '
        data = self.clientKey + ':' + self.clientSecret
        encodedData = base64.b64encode(data)
        string = title + encodedData
        return string

    def getClientKey(self):

        api = self.API_CLIENT_KEY
        j = self.postResponse(api)
        self.clientKey = j['clientkey']
        self.clientSecret = j['clientsecret']

        # print self.clientKey + '--' + self.clientSecret

    def getToken(self):

        api = self.API_TOKEN
        base64EncodedData = self.generateBasicAuthorizationString()
        self.DEFAULT_POST_HEADER['Authorization'] = base64EncodedData

        j = self.postResponse(api)
        self.accessToken = j['access_token']


        # print self.accessToken

