# local imports
import xmatters
import config

# python3 package imports
import logging
import json
from logging.handlers import RotatingFileHandler


# main process
def main() -> object:
    """xMattersPerson Examples:"""
    for i in range(10):
        xm_person.createPerson({'targetName': 'atarget_' + str(i), 'firstName': 'atarget_' + str(i), 'lastName': 'atarget_' + str(i),
             'roles': ['Group Supervisor']})
    xm_person.getPerson('atarget_0')
    xm_person.getPeopleCollection()
    xm_person.removePerson('atarget_0')

    """xMattersDevice Examples:"""
    # user_id = xm_person.getPerson('atarget_1')['id'] # needed for device creation
    # xm_device.createDevice({'name': 'Work Email', 'emailAddress': 'user@xmatters.com', 'deviceType': 'EMAIL', 'owner': user_id})
    # GET, modify, and remove operations also available

    """xMattersGroup Examples:"""
    # group = xm_group.createGroup({'targetName': 'Test Group'})
    # xm_group.modifyGroup({'id': group['id'], 'status': 'INACTIVE'})
    # xm_group.getGroup('Test Group')
    # xm_group.getGroups()
    # xm_group.removeGroup('Test Group')

    """xMattersCollection Examples:"""
    # data = []
    # for x in range(50):
    #     data.append({'targetName': 'target_'+str(x)})
    # response = xm_collection.createGroupsCollection(data, max_threads)
    # data = xm_collection.removeGroupsCollection(data, max_threads)

    # data = []
    # for x in range(50):
    #     data.append({'name': 'target_'+str(x), 'shift':'Default Shift', 'member': 'TestUser'})
    # response = xm_collection.addMemberToShiftCollection(data, max_threads)

    """xMattersRoster Examples:"""
    # xm_roster.addMemberToRoster('Test Group', 'TestUser')
    # xm_roster.getRoster('Test Group')
    # xm_roster.removeMemberFromRoster('Test Group', 'TestUser')

    """xMattersShift Examples:"""
    # xm_shift.createShift('Test Group', {'name': 'Test Shift'})
    # xm_shift.addMemberToShift('Test Group', 'Default Shift', 'TestUser')
    # xm_shift.getShifts('Test Group')
    # xm_shift.getShift('Test Group', 'Default Shift')
    # xm_shift.deleteShift('Test Group', 'Default Shift')

    """xMattersSite Examples:"""
    # xm_site.createSite({'name': 'New Site', 'timezone': 'US/Eastern', 'language': 'EN', 'country': 'USA'})
    # site = xm_site.getSite('Default Site')
    # xm_site.getSites()
    # xm_site.modifySite({'id': site['id'], 'timezone': 'US/Pacific'})


# entry point when file initiated
if __name__ == "__main__":
    # configure the logging
    logging.basicConfig(level=config.logging["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.logging["file_name"], maxBytes=config.logging["max_bytes"],
                                                      backupCount=config.logging["back_up_count"])])
    log = logging.getLogger(__name__)

    # time start
    time_util = xmatters.TimeCalc()
    start = time_util.getTimeNow()
    log.info("Starting Process: " + time_util.formatDateTimeNow(start))

    # instantiate classes
    environment = xmatters.xMattersAPI(config.environment["url"], config.environment["username"],
                                       config.environment["password"])
    xm_person = xmatters.xMattersPerson(environment)
    xm_device = xmatters.xMattersDevice(environment)
    xm_group = xmatters.xMattersGroup(environment)
    xm_collection = xmatters.xMattersCollection(environment)
    xm_roster = xmatters.xMattersRoster(environment)
    xm_shift = xmatters.xMattersShift(environment)
    xm_site = xmatters.xMattersSite(environment)

    max_threads = 15

    # execute the main process
    main()

    # end the duration
    end = time_util.getTimeNow()
    log.info("Process Duration: " + time_util.getDiff(end, start))
