# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersSite(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def getSite(self, id, retry=0):

        def_name = "getSite "

        try:
            self.log.debug(def_name + "Getting Site: " + id)
            url = "/api/xm/1/sites/" + urllib.parse.quote(id, safe='')

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved site: " + json_str["name"] + ". ID = " + json_str["id"])
            elif response.status_code == 404:
                self.log.debug(def_name + "The site could not be found: " + id)
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return getSite(id, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving Site: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def createSite(self, data, retry=0):

        def_name = "createSite "

        try:
            url = "/api/xm/1/sites/"

            name = data["name"]
            self.log.debug(def_name + "Creating Site: " + name + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Created site: " + json_str["name"] + ". ID = " + json_str["id"])
            elif response.status_code == 409:
                self.log.debug(def_name + "Site already exists")
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return createSite(data, retry)
            else:
                self.log.debug(def_name + "Error occurred while creating Site: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def getSites(self, retry=0):

        def_name = "getSite "

        try:
            self.log.debug(def_name + "Getting Sites")
            url = "/api/xm/1/sites"

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved Sites: " + str(response.content))
            elif response.status_code == 404:
                self.log.debug(def_name + "The site could not be found: " + id)
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return getSites(data, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving Sites: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    def modifySite(self, data, retry=0):

        def_name = "modifySite "

        try:
            url = "/api/xm/1/sites/"

            id = data["id"]
            self.log.debug(def_name + "Modifying Site: " + id + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Modified: " + json_str["name"] + ". ID = " + json_str["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return modifySite(data, retry)
            else:
                self.log.debug(def_name + "Error occurred while creating Person: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str
