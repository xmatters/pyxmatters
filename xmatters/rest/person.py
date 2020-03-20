# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersPerson(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def getPerson(self, id, filter="?embed=roles,supervisors", retry=0):

        defName = "getPerson "

        try:
            self.log.debug(defName + "Getting Person: " + id)
            url = "/api/xm/1/people/" + urllib.parse.quote(id, safe='') + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved person: " + jsonStr["targetName"] + ". ID = " + jsonStr["id"])
            elif response.status_code == 404:
                self.log.debug(defName + "The person could not be found: " + id)
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getPerson(id, filter, retry)
            else:
                self.log.error(defName + "Error occurred while retrieving Person: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def getPeople(self, filter="?embed=roles,devices&offset=0&limit=1000", retry=0):

        defName = "getPeople "

        try:
            self.log.debug(defName + "Getting People")
            url = "/api/xm/1/people" + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved people: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getPeople(filter, retry)
            else:
                self.log.error(defName + "Error occurred while retrieving People. Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def createPerson(self, data, retry=0):

        defName = "createPerson "

        try:
            url = "/api/xm/1/people/"

            name = data["targetName"]
            self.log.debug(defName + "Creating Person: " + name + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Created Person: " + jsonStr["targetName"] + ". ID = " + jsonStr["id"])
            elif response.status_code == 409:
                self.log.debug(defName + "Person already exists")
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.createPerson(data, retry)
            else:
                self.log.error(
                    defName + "Error occurred while creating Person: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    # Modify Person:
    #
    # data =  {
    #             "id" : "b2341d69-8b83-4660-b8c8-f2e728f675f9",
    #             "status" : "INACTIVE"
    #         }
    #
    # Reference: https://help.xmatters.com/xmapi/index.html#modify-a-person

    def modifyPerson(self, data, retry=0):

        defName = "modifyPerson "

        try:
            url = "/api/xm/1/people/"

            id = data["id"]
            self.log.debug(defName + "Modifying Person: " + id + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Modified Person: " + jsonStr["targetName"] + ". ID = " + jsonStr["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.modifyPerson(data, retry)
            else:
                self.log.error(
                    defName + "Error occurred while Modifying Person: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e) + " with data: " + str(data))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def removePerson(self, id, retry=0):
        defName = "removePerson "

        try:
            self.log.debug(defName + "Removing Person: " + id)

            url = "/api/xm/1/people/" + id

            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(
                    defName + "Person removed: " + jsonStr["targetName"] + ". Response: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.removePerson(id, retry)
            else:
                self.log.error(
                    defName + "Error occurred while removing Person: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def getPeopleIDs(self, supervisors):
        ids = []
        for supervisor in supervisors:
            xmsupervisor = self.getPerson(supervisor)
            if xmsupervisor:
                ids.append(xmsupervisor["id"])

        return ids

    def getPeopleCollection(self, filter=''):
        defName = "getPeopleCollection "

        try:
            self.log.debug(defName + "Getting People Collection, with filter: " + filter)

            people = self.getPeople("?offset=0&limit=1000" + filter)

            if not people:
                self.log.debug(defName + "People Not Retrieved")
                return None

            total = people["total"]
            count = people["count"]
            p = 0
            users = []

            while p < total:
                for item in people["data"]:
                    users.append(item)

                # increment the pagination count
                p = p + count

                if p < total:
                    people = self.getPeople("?offset="+str(p)+"&limit=1000"+filter)
                    count = people["count"]

        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            users = []

        self.log.debug(defName + "Returning users: " + str(users))

        return users