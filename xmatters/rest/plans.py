# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersPlans(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def getPlan(self, id, filter="?embed=creator,constants,endpoints,forms,propertyDefinitions,integrations", retry=0):

        def_name = "getPlan "

        try:
            self.log.debug(def_name + "Getting Plan: " + id)
            url = "/api/xm/1/plans/" + urllib.parse.quote(id, safe='') + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved plan: " + json_str["name"] + ". ID = " + json_str["id"])
            elif response.status_code == 404:
                self.log.debug(def_name + "The plan could not be found: " + id)
                json_str = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.getPlan(id, filter, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving Plan: " + id + " Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str
