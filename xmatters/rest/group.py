# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersGroup(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def getGroup(self, id, filter="?embed=supervisors", retry=0):

        defName = "getGroup "

        try:
            self.log.debug(defName + "Getting Group: " + id)
            url = "/api/xm/1/groups/" + urllib.parse.quote(id, safe='') + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved group: " + jsonStr["targetName"] + ". ID = " + jsonStr["id"])
            elif response.status_code == 404:
                self.log.debug(defName + "The group could not be found: " + id)
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getGroup(id, filter, retry)
            else:
                self.log.debug(defName + "Error occurred while retrieving Group: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def getGroups(self, filter="?offset=0&limit=1000", retry=0):

        defName = "getGroups "

        try:
            self.log.debug(defName + "Getting Groups")

            url = "/api/xm/1/groups" + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved groups: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getGroups(name, fitler, retry)
            else:
                self.log.debug(defName + "Error occurred while retrieving Groups. Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr


    def createGroup(self, data, retry=0):

        defName = "createGroup "

        try:
            url = "/api/xm/1/groups/"
            name = data["targetName"]
            self.log.debug(defName + "Creating Group: " + name + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Created group: " + jsonStr["targetName"] + ". ID = " + jsonStr["id"])
            elif response.status_code == 409:
                self.log.debug(defName + "Group already exists")
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.createGroup(data, retry)
            else:
                self.log.debug(defName + "Error occurred while creating Group: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr


    # Modify Group
    #
    #     data = {
    #                 "id" : "138e9245-bded-445f-916b-dda07932b679",
    #                 "recipientType": "GROUP",
    #                 "description": "Executive team members"
    #            }
    #
    # Reference: https://help.xmatters.com/xmapi/index.html#modify-a-group
    
    def modifyGroup(self, data, retry=0):

        defName = "modifyGroup "

        try:
            url = "/api/xm/1/groups/"

            id = data["id"]
            self.log.debug(defName + "Modifying Group: " + id + " with " + str(data))
            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Modified group: " + jsonStr["targetName"] + ". ID = " + jsonStr["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.modifyGroup(data, retry)
            else:
                self.log.debug(defName + "Error occurred while modifying group: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr


    def removeGroup(self, id, retry=0):
        defName = "removeGroup "

        try:
            self.log.debug(defName + "Removing Group: " + id)

            url = "/api/xm/1/groups/" + urllib.parse.quote(id, safe='')

            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Group removed: " + jsonStr["targetName"] + ". Response: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.removeGroup(id, retry)
            else:
                self.log.debug(defName + "Error occurred while removing Group: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr
