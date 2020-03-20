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

        def_name = "getPerson "

        try:
            self.log.debug(def_name + "Getting Person: " + id)
            url = "/api/xm/1/people/" + urllib.parse.quote(id, safe='') + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved person: " + json_str["targetName"] + ". ID = " + json_str["id"])
            elif response.status_code == 404:
                self.log.debug(def_name + "The person could not be found: " + id)
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getPerson(id, filter, retry)
            else:
                self.log.error(def_name + "Error occurred while retrieving Person: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def getPeople(self, filter="?embed=roles,devices&offset=0&limit=1000", retry=0):

        def_name = "getPeople "

        try:
            self.log.debug(def_name + "Getting People")
            url = "/api/xm/1/people" + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved people: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getPeople(filter, retry)
            else:
                self.log.error(def_name + "Error occurred while retrieving People. Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def createPerson(self, data, retry=0):

        def_name = "createPerson "

        try:
            url = "/api/xm/1/people/"

            name = data["targetName"]
            self.log.debug(def_name + "Creating Person: " + name + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Created Person: " + json_str["targetName"] + ". ID = " + json_str["id"])
            elif response.status_code == 409:
                self.log.debug(def_name + "Person already exists")
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.createPerson(data, retry)
            else:
                self.log.error(
                    def_name + "Error occurred while creating Person: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    # Modify Person:
    #
    # data =  {
    #             "id" : "b2341d69-8b83-4660-b8c8-f2e728f675f9",
    #             "status" : "INACTIVE"
    #         }
    #
    # Reference: https://help.xmatters.com/xmapi/index.html#modify-a-person

    def modifyPerson(self, data, retry=0):

        def_name = "modifyPerson "

        try:
            url = "/api/xm/1/people/"

            id = data["id"]
            self.log.debug(def_name + "Modifying Person: " + id + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Modified Person: " + json_str["targetName"] + ". ID = " + json_str["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.modifyPerson(data, retry)
            else:
                self.log.error(
                    def_name + "Error occurred while Modifying Person: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e) + " with data: " + str(data))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def removePerson(self, id, retry=0):
        def_name = "removePerson "

        try:
            self.log.debug(def_name + "Removing Person: " + id)

            url = "/api/xm/1/people/" + id

            response = self.request.delete(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(
                    def_name + "Person removed: " + json_str["targetName"] + ". Response: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.removePerson(id, retry)
            else:
                self.log.error(
                    def_name + "Error occurred while removing Person: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def getPeopleIDs(self, supervisors):
        ids = []
        for supervisor in supervisors:
            xmsupervisor = self.getPerson(supervisor)
            if xmsupervisor:
                ids.append(xmsupervisor["id"])

        return ids

    def getPeopleCollection(self, filter=''):
        def_name = "getPeopleCollection "

        try:
            self.log.debug(def_name + "Getting People Collection, with filter: " + filter)

            people = self.getPeople("?offset=0&limit=1000" + filter)

            if not people:
                self.log.debug(def_name + "People Not Retrieved")
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
            self.log.error(def_name + "Unexpected exception: " + str(e))
            users = []

        self.log.debug(def_name + "Returning users: " + json.dumps(users))

        return users