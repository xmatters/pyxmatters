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

        def_name = "createDynamicTeam "

        try:
            url = "/api/xm/1/dynamic-teams/"
            name = data["targetName"]
            self.log.debug(def_name + "Creating Dynamic Team: " + name + " with " + json.dumps(data))

            response = self.request.post(data, url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Created Dynamic Team: " + str(response.content))
            elif response.status_code == 409:
                self.log.debug(def_name + "Dynamic Team already exists")
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.createDynamicTeam(data, retry)
            else:
                self.log.debug(
                    def_name + "Error occurred while creating Dynamic Team: " + name + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str