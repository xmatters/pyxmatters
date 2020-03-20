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

        defName = "getSite "

        filter = None

        try:
            self.log.debug(defName + "Getting Site: " + id)
            url = "/api/xm/1/sites/" + urllib.parse.quote(id, safe='')

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved site: " + jsonStr["name"] + ". ID = " + jsonStr["id"])
            elif response.status_code == 404:
                self.log.debug(defName + "The site could not be found: " + id)
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return getSite(id, retry)
            else:
                self.log.debug(defName + "Error occurred while retrieving Site: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def createSite(self, data, retry=0):

        defName = "createSite "

        try:
            url = "/api/xm/1/sites/"

            name = data["name"]
            self.log.debug(defName + "Creating Site: " + name + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Created site: " + jsonStr["name"] + ". ID = " + jsonStr["id"])
            elif response.status_code == 409:
                self.log.debug(defName + "Site already exists")
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return createSite(data, retry)
            else:
                self.log.debug(defName + "Error occurred while creating Site: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def getSites(self, retry=0):

        defName = "getSite "

        try:
            self.log.debug(defName + "Getting Sites")
            url = "/api/xm/1/sites"

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved Sites: " + str(response.content))
            elif response.status_code == 404:
                self.log.debug(defName + "The site could not be found: " + id)
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return getSites(data, retry)
            else:
                self.log.debug(defName + "Error occurred while retrieving Sites: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr

    def modifySite(self, data, retry=0):

        defName = "modifySite "

        try:
            url = "/api/xm/1/sites/"

            id = data["id"]
            self.log.debug(defName + "Modifying Site: " + id + " with " + str(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Modified: " + jsonStr["name"] + ". ID = " + jsonStr["id"])
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return modifySite(data, retry)
            else:
                self.log.debug(defName + "Error occurred while creating Person: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr
