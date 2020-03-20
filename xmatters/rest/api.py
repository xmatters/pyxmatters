import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
import json
import ssl
import time
import logging


class xMattersAPI(object):

    def __init__(self, url, username, password, log=None):
        self.url = url
        self.username = username
        self.password = password
        self.log = logging.getLogger(__name__)
        self.max_retry = 3

    def execute(self, function, *args, **kwargs):
        retry = 0
        while retry < self.max_retry:
            try:
                response = function(*args, **kwargs)
                retry = self.max_retry
            except Exception as e:
                self.log.error("Unexpected exception:" + str(e))
                retry = retry+1
                response = {}
        return response

    def post(self, data, path, headers=None):
        return self.execute(requests.post, self.url + path, auth=HTTPBasicAuth(self.username, self.password), headers={"Content-Type": "application/json"} if headers == None else headers, data=json.dumps(data))

    def put(self, data, path, headers=None):
        return self.execute(requests.put, self.url + path, auth=HTTPBasicAuth(self.username, self.password), headers={"Content-Type": "application/json"} if headers == None else headers, data=json.dumps(data))

    def get(self, path):
        return self.execute(requests.get, self.url + path, auth=HTTPBasicAuth(self.username, self.password))

    def delete(self, path):
        return self.execute(requests.delete, self.url + path, auth=HTTPBasicAuth(self.username, self.password))

    def statusCodeSuccess(statusCode):
        return statusCode >= 200 and statusCode <= 299

    def tooManyRequests(statusCode):
        if statusCode == 429:
            time.sleep(30)
            return True
        else:
            return False
