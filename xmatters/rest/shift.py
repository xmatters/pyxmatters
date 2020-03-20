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

        def_name = "addMemberToShift "

        try:
            self.log.debug(def_name + "adding member " + memberId + " to group " + groupId + " shift " + shiftId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts/" + urllib.parse.quote(shiftId, safe='') + "/members"

            data = {
                "recipient": {
                    "id": str(memberId),
                    "recipientType": "PERSON"
                }
            }

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(
                    def_name + json.dumps(json_str))
                self.log.debug(
                    def_name + "Added member: " + json_str["recipient"]["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.addMemberToShift(groupId, shiftId, memberId, retry)
            elif response.status_code == 404:
                self.log.error(
                    def_name + "Failed to add member: " + memberId + " to Group: " + groupId + ". Group or User does not exist. HTTP Response: " + str(response.content))
                json_str = None
            else:
                self.log.error(
                    def_name + "Failed to add member: " + groupId + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(
                def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def getShift(self, groupId, shiftId, retry=0):

        def_name = "getShift "

        try:
            self.log.debug(def_name + "Getting Group: " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts/" + urllib.parse.quote(shiftId, safe='')

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(
                    def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved shift: " + json_str["name"] + ". ID = " + json_str["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getShift(name, groupId, shiftId, retry)
            else:
                self.log.error(
                    def_name + "Failed retrieving shift: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(
                def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def getShifts(self, groupId, retry=0):

        def_name = "getShifts "

        try:
            self.log.debug(def_name + "Getting Group Shifts: " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts"

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(
                    def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved shifts: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getShifts(groupId, retry)
            else:
                self.log.error(
                    def_name + "Failed retrieving shift: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(
                def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def createShift(self, groupId, data, retry=0):

        def_name = "createShift "

        try:
            self.log.debug(def_name + "Creating Shift, for " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts"

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Created shift: " + groupId)
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.createShift(groupId, data, retry)
            else:
                self.log.error(def_name + "Failed creating shift, for Group: " + groupId + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(
                def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def deleteShift(self, groupId, shiftId, retry):

        def_name = "deleteShift "

        try:
            self.log.debug(def_name + "Getting Group: " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/shifts/" + urllib.parse.quote(shiftId, safe='')
            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(
                    def_name + json.dumps(json_str))
                self.log.debug(def_name + "Deleted shift: " + shiftId)
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.deleteShift(groupId, groupId, shiftId, retry)
            else:
                self.log.error(def_name + "Failed deleting shift: " + shiftId + " from Group: " + groupId + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(
                def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str
