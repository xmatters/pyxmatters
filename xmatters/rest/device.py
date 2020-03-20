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

        def_name = "getDevice "

        try:
            self.log.debug(def_name + "Getting Device: " + id)
            url = "/api/xm/1/devices/" + urllib.parse.quote(id, safe='') + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved device: " + json_str["name"] + ". device type = " + json_str["deviceType"])
            elif response.status_code == 404:
                self.log.debug(def_name + "The device could not be found: " + id)
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getDevice(id, filter, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving Device: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def getDevices(self, filter="?embed=timeframes", retry=0):

        def_name = "getDevices "

        try:
            self.log.debug(def_name + "Getting Devices")
            url = "/api/xm/1/devices" + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved people: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getDevices(filter, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving Devices. Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def createDevice(self, data, retry=0):

        def_name = "createDevice "

        try:
            url = "/api/xm/1/devices"

            name = data["name"]
            owner = data["owner"]
            self.log.debug(def_name + "Creating Device: " + name + " for owner: " + owner)

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Created Device: " + json_str["name"] + ". Owner targetName = " + json_str["owner"]["targetName"])
            elif response.status_code == 409:
                self.log.debug(def_name + "Device already exists")
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.createDevice(data, retry)
            else:
                self.log.debug(def_name + "Error occurred while creating Device: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def modifyDevice(self, data, retry=0):

        def_name = "modifyDevice "

        try:
            url = "/api/xm/1/devices/"

            id = data["id"]
            self.log.debug(def_name + "Modifying Devices: " + id + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Modified Device: " + json_str["id"] + ". Owner targetName = " + json_str["owner"]["targetName"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.modifyDEvice(data, retry)
            else:
                self.log.debug(def_name + "Error occurred while Modifying Device: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e) + " with data: " + str(data))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str


    def removeDevice(self, id, retry=0):
        def_name = "removeDevice "

        try:
            self.log.debug(def_name + "Removing Device: " + id)

            url = "/api/xm/1/devices/" + id

            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Device removed: " + json_str["id"] + ". Response: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.removeDevice(id, retry)
            else:
                self.log.debug(def_name + "Error occurred while removing Device: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str
