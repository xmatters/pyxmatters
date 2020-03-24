# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersOnCall(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def getOnCallCollection(self, filter=""):

        def_name = "getOnCallCollection "
        try:
            filter = self.__parseFilter(filter)
            self.log.debug(def_name + "Getting OnCall Collection, with filter: " + filter)

            groups = self.__getOnCallGroups("?offset=0&limit=1000&membersPerShift=100" + filter)

            if not groups:
                self.log.debug(def_name + "OnCall Not Retrieved")
                return None

            total = groups["total"]
            count = groups["count"]
            p = 0
            oncall = []

            while p < total:
                for item in groups["data"]:

                    if self.__hasNextLink(item["members"]):
                        continue_to_get_members = True
                        member_link = None
                        while continue_to_get_members:

                            if not member_link:  # only execute below on first iteration
                                members = self.__getOnCallMembers(item["members"]["links"]["next"])
                            else:  # for all other iterations
                                members = self.__getOnCallMembers(member_link)

                            if members:  # only execute if there are members to process
                                for member in members["data"]:
                                    item["members"]["data"].append(member)

                                # get next series
                                if self.__hasNextLink(members):
                                    member_link = members["links"]["next"]
                                else:
                                    continue_to_get_members = False
                            else:
                                continue_to_get_members = False

                    # let"s clear the links
                    item["members"].pop("links", None)
                    oncall.append(item)

                # increment the pagination count
                p = p + count

                if p < total:
                    groups = self.__getOnCallGroups("?offset=" + str(p) + "&limit=1000" + filter)
                    count = groups["count"]

        except Exception as e:
            self.log.error(def_name + "Unexpected exception: " + str(e))
            oncall = []

        self.log.debug(def_name + "Returning OnCall: " + json.dumps(oncall))

        return oncall

    # private method
    def __getOnCallGroups(self, filter="?offset=0&limit=1000", retry=0):

        def_name = "__getOnCallGroups "

        try:
            self.log.debug(def_name + "Getting OnCall for Groups")

            url = "/api/xm/1/on-call" + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved OnCall: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.__getOnCallGroups(filter, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving OnCall. Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    # private method
    def __getOnCallMembers(self, filter, retry=0):

        def_name = "__getOnCallMembers "

        try:
            self.log.debug(def_name + "Getting OnCall for Members")

            url = filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                json_str = response.json()
                self.log.debug(def_name + json.dumps(json_str))
                self.log.debug(def_name + "Retrieved OnCall: " + str(response.content))
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(def_name + "Status Code: " + str(response.status_code) + ". Too many requests.")
                if retry < 3:
                    retry = retry + 1
                    self.log.error(def_name + "Retrying, retry count: " + str(retry))
                    return self.__getOnCallMembers(filter, retry)
            else:
                self.log.debug(def_name + "Error occurred while retrieving OnCall. Response: " + str(response.content))
                json_str = None
        except Exception as e:
            self.log.error(def_name + "Unexpected exception:" + str(e))
            json_str = None

        self.log.debug(def_name + "Returning response: " + str(json_str))

        return json_str

    # private method
    # purpose of this filter is to remove membersPerShift, offset, and limit
    def __parseFilter(self, filter=""):
        def_name = "__parseFilter "
        new_filter = ""

        try:
            for filter_str in filter.split("&"):
                if filter_str == "":
                    new_filter = new_filter + filter_str
                else:
                    if filter_str.find("membersPerShift") == -1 and filter_str.find("offset") == -1 and filter_str.find(
                            "limit") == -1:
                        new_filter = new_filter + "&" + filter_str
        except Exception as e:
            self.log.error(def_name + "Unexpected exception: " + str(e))

        return new_filter

    def __hasNextLink(self, obj):
        has = True
        try:
            # an exception will throw if it doesn't exist
            obj["links"]["next"]
        except:
            has = False
        return has