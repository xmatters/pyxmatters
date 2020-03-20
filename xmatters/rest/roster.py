import logging
import urllib.parse
from .api import xMattersAPI
import json


class xMattersRoster(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)


    # groupId = (id) or name (targetName) of the group.

    def addMemberToRoster(self, groupId, memberId, retry=0):

        defName = "addMemberToRoster "

        try:
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/members"

            data = {
                    "id": str(memberId),
                    "recipientType": "PERSON"
            }

            response = self.request.post(data, url)
            self.log.debug(defName + "adding member "+memberId+" to group roster " + groupId + " with " + str(data))
            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Added member: " + jsonStr["targetName"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.addMemberToRoster(groupId, memberId, retry)
            elif response.status_code == 404:
                self.log.error(
                    defName + "Failed to add member: " + memberId + " to Group Roster: "+memberId +". Group or User does not exist. HTTP Response: " + str(response.content))
                jsonStr = None
            else:
                self.log.error(
                    defName + "Failed to add member: " + memberId + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(
                defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr


    # groupId = (id) or name (targetName) of the group.

    def removeMemberFromRoster(self, groupId, memberId, retry=0):

        defName = "removeMemberFromRoster "

        try:
            self.log.debug(defName + "removing member "+memberId+" from group roster " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/members/"+urllib.parse.quote(memberId, safe='')

            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(
                    defName + json.dumps(jsonStr))
                self.log.debug(
                    defName + "Removed member: " + jsonStr["member"]["targetName"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.removeMemberFromRoster(groupId, memberId, retry)
            elif response.status_code == 404:
                self.log.error(
                    defName + "Failed to remove member: " + memberId + " from Group Roster: "+memberId +". User does not exist. HTTP Response: " + str(response.content))
                jsonStr = None
            else:
                self.log.error(
                    defName + "Failed to add member: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(
                defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    # groupId = (id) or name (targetName) of the group.

    def getRoster(self, groupId, filter="&offset=0&limit=1000", retry=0):

        defName = "getRoster "

        try:
            self.log.debug(defName + "Getting Group Roster: " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/members?embed=shifts" +filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + " Retrieved Group Roster: "+ json.dumps(jsonStr))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getRoster(groupId, filter, retry)
            else:
                self.log.error(defName + "Failed retrieving Group Roster: " + groupId + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(
                defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    # groupId = (id) or name (targetName) of the group.
    def getRosterCollection(self, groupId):

        defName = "getRosterCollection "

        try:
            self.log.debug(defName + "Getting Group Roster Collection: " + groupId)

            roster = self.getRoster(groupId, "&offset=0&limit=1000")

            if not roster:
                self.log.debug(defName + "Group Not Retrieved: " + groupId)
                return None

            total = roster["total"]
            count = roster["count"]
            p = 0
            members = set()

            while p < total:
                for item in roster["data"]:
                    members.add(item["member"]["targetName"])

                # increment the pagination count
                p = p + count

                if p < total:
                    roster = self.getRoster(groupId, "&offset="+str(p)+"&limit=1000")
                    count = roster["count"]

        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            members = set()

        self.log.debug(defName + "Returning members: " + str(members))

        return members
