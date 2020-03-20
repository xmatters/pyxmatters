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

        def_name = "getGroup "

        try:
            self.log.debug(def_name + "Getting Group: " + id)
            url = "/api/xm/1/groups/" + urllib.parse.quote(id, safe='') + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved group: " + json_str["targetName"] + ". ID = " + json_str["id"])
            elif response.status_code == 404:
                self.log.debug(def_name + "The group could not be found: " + id)
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getGroup(id, filter, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving Group: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def getGroups(self, filter="?offset=0&limit=1000", retry=0):

        def_name = "getGroups "

        try:
            self.log.debug(def_name + "Getting Groups")

            url = "/api/xm/1/groups" + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved groups: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getGroups(name, fitler, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving Groups. Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str


    def createGroup(self, data, retry=0):

        def_name = "createGroup "

        try:
            url = "/api/xm/1/groups/"
            name = data["targetName"]
            self.log.debug(def_name + "Creating Group: " + name + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Created group: " + json_str["targetName"] + ". ID = " + json_str["id"])
            elif response.status_code == 409:
                self.log.debug(def_name + "Group already exists")
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.createGroup(data, retry)
            else:
                self.log.debug(def_name + "Error occurred while creating Group: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str


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

        def_name = "modifyGroup "

        try:
            url = "/api/xm/1/groups/"

            id = data["id"]
            self.log.debug(def_name + "Modifying Group: " + id + " with " + str(data))
            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Modified group: " + json_str["targetName"] + ". ID = " + json_str["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.modifyGroup(data, retry)
            else:
                self.log.debug(def_name + "Error occurred while modifying group: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str


    def removeGroup(self, id, retry=0):
        def_name = "removeGroup "

        try:
            self.log.debug(def_name + "Removing Group: " + id)

            url = "/api/xm/1/groups/" + urllib.parse.quote(id, safe='')

            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Group removed: " + json_str["targetName"] + ". Response: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.removeGroup(id, retry)
            else:
                self.log.debug(def_name + "Error occurred while removing Group: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def getGroupCollection(self, filter=''):
        def_name = "getGroupCollection "

        try:
            self.log.debug(def_name + "Getting Groups Collection, with filter: " + filter)

            group = self.getGroups("?offset=0&limit=1000" + filter)

            if not group:
                self.log.debug(def_name + "Groups Not Retrieved")
                return None

            total = group["total"]
            count = group["count"]
            p = 0
            groups = []

            while p < total:
                for item in group["data"]:
                    groups.append(item)

                # increment the pagination count
                p = p + count

                if p < total:
                    group = self.getGroups("?offset="+str(p)+"&limit=1000"+filter)
                    count = group["count"]

        except Exception as e:
            self.log.error(def_name + 'Unexpected exception: ' + str(e))
            groups = []

        self.log.debug(def_name + "Returning groups: " + json.dumps(groups))

        return groups