# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersDynamicTeams(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def createDynamicTeam(self, data, retry=0):

        defName = "createDynamicTeam "

        try:
            url = "/api/xm/1/dynamic-teams/"
            name = data["targetName"]
            self.log.debug(defName + "Creating Dynamic Team: " + name + " with " + json.dumps(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Created Dynamic Team: " + str(response.content))
            elif response.status_code == 409:
                self.log.debug(defName + "Dynamic Team already exists")
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.createDynamicTeam(data, retry)
            else:
                self.log.debug(
                    defName + "Error occurred while creating Dynamic Team: " + name + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr