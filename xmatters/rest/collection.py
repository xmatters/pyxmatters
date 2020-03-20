# standard python modules
import logging
import threading
import math

# import all local modules from the rest package
from . import *


class xMattersCollectionThread(object):

    # constructor
    def __init__(self, request):
        self.log = logging.getLogger(__name__)
        self.request = request

    def createCollection(self, data, max_threads, function):
        bucketSize = int(math.ceil(float(len(data)) / float(max_threads)))
        threads = []
        for n in range(max_threads):
            slice = data[n * int(bucketSize): (n + 1) * int(bucketSize)]
            if len(slice) > 0:
                process = threading.Thread(target=function, args=(n, slice, ))
                process.start()
                threads.append(process)

        # Join all threads before proceeding
        for process in threads:
            process.join()

        return process

class xMattersCollection(xMattersCollectionThread):

    # constructor
    def __init__(self, *args, **kwargs):
        super(xMattersCollection, self).__init__(*args, **kwargs)
        self.succeed = []
        self.fail = []

    # def to Create Groups
    def createGroupsCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        self.createCollection(data, max_threads, self.createGroups)
        return {"succeed": self.succeed, "fail": self.fail}

    def createGroups(self, thread, data):
        xmGroup = xMattersGroup(self.request)
        for x in range(len(data)):
            self.log.debug("Thread number: " + str(thread) + " Creating Group: " + data[x]["targetName"])
            response = xmGroup.createGroup(data[x])
            if response:
                self.succeed.append(data[x]["targetName"])
            else:
                self.fail.append(data[x]["targetName"])

    # def to add Members
    def addMemberToShiftCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        self.createCollection(data, max_threads, self.addMembersToShift)
        return {"succeed": self.succeed, "fail": self.fail}

    def addMembersToShift(self, thread, data):
        xmShift = xMattersShift(self.request)
        for x in range(len(data)):
            self.log.debug("Thread number: " + str(thread) + " Adding Member: " + data[x]["member"] + " to Shift: "+data[x]["shift"]+" in Group: " + data[x]["name"])
            response = xmShift.addMemberToShift(data[x]["name"], data[x]["shift"], data[x]["member"])
            if response:
                self.succeed.append(data[x]["member"])
            else:
                self.fail.append(data[x]["member"])

    # def to add Members
    def addMemberToRosterCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        self.createCollection(data, max_threads, self.addMembersToRoster)
        return {"succeed": self.succeed, "fail": self.fail}

    def addMembersToRoster(self, thread, data):
        xmRoster = xMattersRoster(self.request)
        for x in range(len(data)):
            self.log.debug("Thread number: " + str(thread) + " Adding Member: " + data[x]["member"] + " to Roster for Group: " + data[x]["name"])
            response = xmRoster.addMemberToRoster(data[x]["name"], data[x]["member"])
            if response:
                self.succeed.append(data[x]["member"])
            else:
                self.fail.append(data[x]["member"])
    # def to Create Groups
    def removeGroupsCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        self.createCollection(data, max_threads, self.removeGroups)
        return {"succeed": self.succeed, "fail": self.fail}

    def removeGroups(self, thread, data):
        xmGroup = xMattersGroup(self.request)
        for x in range(len(data)):
            self.log.debug("Thread number: " + str(thread) + " Removing Group: " + data[x]["targetName"])
            response = xmGroup.removeGroup(data[x]["targetName"])
            if response:
                self.succeed.append(data[x]["targetName"])
            else:
                self.fail.append(data[x]["targetName"])

    # def to Create Groups
    def createOrModifyGroupsCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        self.createCollection(data, max_threads, self.createOrModifyGroups)
        return {"succeed": self.succeed, "fail": self.fail}

    # function accepts an array of supervisor names and retrieves them
    def createOrModifyGroups(self, thread, data):
        xmGroup = xMattersGroup(self.request)
        xmPerson = xMattersPerson(self.request)
        for x in range(len(data)):
            self.log.debug("Thread number: " + str(thread) + " Creating Group: " + data[x]["targetName"])

            # function accepts an array of supervisor names and retrieves them
            data[x]["supervisors"] = xmPerson.getPeopleIDs(data[x]["supervisors"])
            exist = xmGroup.getGroup(data[x]["targetName"])
            if (exist is None):
                response = xmGroup.createGroup(data[x])
            elif (exist):
                data[x]["id"] = exist["id"]
                response = xmGroup.modifyGroup(data[x])
            if response:
                self.succeed.append(data[x]["targetName"])
            else:
                self.fail.append(data[x]["targetName"])

    # def to Modify Persons
    def modifyPeopleCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        self.createCollection(data, max_threads, self.modifyPeople)
        return {"succeed": self.succeed, "fail": self.fail}

    def modifyPeople(self, thread, data):
        xmPerson = xMattersPerson(self.request)
        for x in range(len(data)):
            self.log.debug("Thread number: " + str(thread) + " Modifying User: " + data[x]["targetName"])
            response = xmPerson.modifyPerson(data[x])
            if response:
                self.succeed.append(data[x]["targetName"])
            else:
                self.fail.append(data[x]["targetName"])

    # def modifyPeople(self, thread, data):
    #     xmPerson = xMattersPerson(self.request)
    #     for x in range(len(data)):
    #         user = xmPerson.getPerson(data[x]["targetName"])
    #         if user:
    #             data[x]["id"] = user["id"]
    #             for role in user["roles"]["data"]:
    #                 data[x]["roles"].append(role["name"])
    #             self.log.debug("Thread number: " + str(thread) + " Modifying User: " + data[x]["targetName"])
    #             # print("Thread number: " + str(thread) + " Modifying User: " + data[x]["targetName"])
    #             response = xmPerson.modifyPerson(data[x])
    #             if response:
    #                 self.succeed.append(data[x]["targetName"])
    #             else:
    #                 self.fail.append(data[x]["targetName"])
    #         else:
    #             self.fail.append(data[x]["targetName"])
