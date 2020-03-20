import logging
import urllib.parse
from .api import xMattersAPI
import json


class xMattersShift(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def addMemberToShift(self, groupId, shiftId, memberId, retry=0):

        defName = "addMemberToShift "

        try:
            self.log.debug(defName + "adding member " + memberId + " to group " + groupId + " shift " + shiftId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts/" + urllib.parse.quote(shiftId, safe='') + "/members"

            data = {
                "recipient": {
                    "id": str(memberId),
                    "recipientType": "PERSON"
                }
            }

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(
                    defName + json.dumps(jsonStr))
                self.log.debug(
                    defName + "Added member: " + jsonStr["recipient"]["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.addMemberToShift(groupId, shiftId, memberId, retry)
            elif response.status_code == 404:
                self.log.error(
                    defName + "Failed to add member: " + memberId + " to Group: " + groupId + ". Group or User does not exist. HTTP Response: " + str(response.content))
                jsonStr = None
            else:
                self.log.error(
                    defName + "Failed to add member: " + groupId + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(
                defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def getShift(self, groupId, shiftId, retry=0):

        defName = "getShift "

        try:
            self.log.debug(defName + "Getting Group: " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts/" + urllib.parse.quote(shiftId, safe='')

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(
                    defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved shift: " + jsonStr["name"] + ". ID = " + jsonStr["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getShift(name, groupId, shiftId, retry)
            else:
                self.log.error(
                    defName + "Failed retrieving shift: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(
                defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def getShifts(self, groupId, retry=0):

        defName = "getShifts "

        try:
            self.log.debug(defName + "Getting Group Shifts: " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts"

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(
                    defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved shifts: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getShifts(groupId, retry)
            else:
                self.log.error(
                    defName + "Failed retrieving shift: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(
                defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def createShift(self, groupId, data, retry=0):

        defName = "createShift "

        try:
            self.log.debug(defName + "Creating Shift, for " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts"

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Created shift: " + groupId)
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.createShift(groupId, data, retry)
            else:
                self.log.error(defName + "Failed creating shift, for Group: " + groupId + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(
                defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def deleteShift(self, groupId, shiftId, retry):

        defName = "deleteShift "

        try:
            self.log.debug(defName + "Getting Group: " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts/" + urllib.parse.quote(shiftId, safe='')
            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(
                    defName + json.dumps(jsonStr))
                self.log.debug(defName + "Deleted shift: " + shiftId)
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.deleteShift(groupId, groupId, shiftId, retry)
            else:
                self.log.error(defName + "Failed deleting shift: " + shiftId + " from Group: " + groupId + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(
                defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr
