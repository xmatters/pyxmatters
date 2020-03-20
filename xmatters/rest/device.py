# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersDevice(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def getDevice(self, id, filter="?embed=timeframes", retry=0):

        defName = "getDevice "

        try:
            self.log.debug(defName + "Getting Device: " + id)
            url = "/api/xm/1/devices/" + urllib.parse.quote(id, safe='') + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved device: " + jsonStr["name"] + ". device type = " + jsonStr["deviceType"])
            elif response.status_code == 404:
                self.log.debug(defName + "The device could not be found: " + id)
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getDevice(id, filter, retry)
            else:
                self.log.debug(defName + "Error occurred while retrieving Device: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def getDevices(self, filter="?embed=timeframes", retry=0):

        defName = "getDevices "

        try:
            self.log.debug(defName + "Getting Devices")
            url = "/api/xm/1/devices" + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved people: " +  str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getDevices(filter, retry)
            else:
                self.log.debug(defName + "Error occurred while retrieving Devices. Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def createDevice(self, data, retry=0):

        defName = "createDevice "

        try:
            url = "/api/xm/1/devices"

            name = data["name"]
            owner = data["owner"]
            self.log.debug(defName + "Creating Device: " + name + " for owner: " + owner)

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Created Device: " + jsonStr["name"] + ". Owner targetName = " + jsonStr["owner"]["targetName"])
            elif response.status_code == 409:
                self.log.debug(defName + "Device already exists")
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.createDevice(data, retry)
            else:
                self.log.debug(defName + "Error occurred while creating Device: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def modifyDevice(self, data, retry=0):

        defName = "modifyDevice "

        try:
            url = "/api/xm/1/devices/"

            id = data["id"]
            self.log.debug(defName + "Modifying Devices: " + id + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Modified Device: " + jsonStr["id"] + ". Owner targetName = " + jsonStr["owner"]["targetName"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.modifyDEvice(data, retry)
            else:
                self.log.debug(defName + "Error occurred while Modifying Device: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e) + " with data: " + str(data))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr


    def removeDevice(self, id, retry=0):
        defName = "removeDevice "

        try:
            self.log.debug(defName + "Removing Device: " + id)

            url = "/api/xm/1/devices/" + id

            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Device removed: " + jsonStr["id"] + ". Response: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.removeDevice(id, retry)
            else:
                self.log.debug(defName + "Error occurred while removing Device: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr
