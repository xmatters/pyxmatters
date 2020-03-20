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

        def_name = "addMemberToRoster "

        try:
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/members"

            data = {
                    "id": str(memberId),
                    "recipientType": "PERSON"
            }

            response = self.request.post(data, url)
            self.log.debug(def_name + "adding member "+memberId+" to group roster " + groupId + " with " + str(data))
            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Added member: " + json_str["targetName"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.addMemberToRoster(groupId, memberId, retry)
            elif response.status_code == 404:
                self.log.error(
                    def_name + "Failed to add member: " + memberId + " to Group Roster: "+memberId +". Group or User does not exist. HTTP Response: " + str(response.content))
                json_str = None
            else:
                self.log.error(
                    def_name + "Failed to add member: " + memberId + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(
                def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str


    # groupId = (id) or name (targetName) of the group.

    def removeMemberFromRoster(self, groupId, memberId, retry=0):

        def_name = "removeMemberFromRoster "

        try:
            self.log.debug(def_name + "removing member "+memberId+" from group roster " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/members/"+urllib.parse.quote(memberId, safe='')

            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(
                    def_name + json.dumps(json_str))
                self.log.debug(
                    def_name + "Removed member: " + json_str["member"]["targetName"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.removeMemberFromRoster(groupId, memberId, retry)
            elif response.status_code == 404:
                self.log.error(
                    def_name + "Failed to remove member: " + memberId + " from Group Roster: "+memberId +". User does not exist. HTTP Response: " + str(response.content))
                json_str = None
            else:
                self.log.error(
                    def_name + "Failed to add member: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(
                def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    # groupId = (id) or name (targetName) of the group.

    def getRoster(self, groupId, filter="&offset=0&limit=1000", retry=0):

        def_name = "getRoster "

        try:
            self.log.debug(def_name + "Getting Group Roster: " + groupId)
            url = "/api/xm/1/groups/" + urllib.parse.quote(groupId, safe='') + "/members?embed=shifts" +filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + " Retrieved Group Roster: "+ json.dumps(json_str))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getRoster(groupId, filter, retry)
            else:
                self.log.error(def_name + "Failed retrieving Group Roster: " + groupId + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(
                def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    # groupId = (id) or name (targetName) of the group.
    def getRosterCollection(self, groupId):

        def_name = "getRosterCollection "

        try:
            self.log.debug(def_name + "Getting Group Roster Collection: " + groupId)

            roster = self.getRoster(groupId, "&offset=0&limit=1000")

            if not roster:
                self.log.debug(def_name + "Group Not Retrieved: " + groupId)
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
            self.log.error(def_name + "Unexpected exception:" + str(e))
            members = set()

        self.log.debug(def_name + "Returning members: " + str(members))

        return members
