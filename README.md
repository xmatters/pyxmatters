# pyxmatters
The pyxmatters package provides a rest api interface with xMatters. There are also file reading capabilities to assist with synchronizing data.

## Install, Upgrades, and use of pyxmatters
For Production use it is **strongly** recommended to download the pyxmatters package, specifically the xmatters directory, and set it alongside the script leveraging it. 

For installing locally with the understanding the package will change and could break your script, follow the steps below:

To Install via pip, navigate to the terminal and enter:
* `pip3 install pyxmatters`

To Upgrade via pip, navigate to terminal and enter:
* `sudo pip3 install --upgrade --force-reinstall pyxmatters`

## Overview of the pyxmatters package

### pyxmatters/rest
This directory provides user, device, group, and site rest api capabilities.

#### pyxmatters/rest/person.py
```
import xmatters
import logging
logging.basicConfig(filename='log.log',level=10,datefmt='%m-%d-%Y %H:%M:%S',format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_person = xmatters.xMattersPerson(environment)

log.info("Starting Process")
xm_person.create_person({'targetName': 'username', 'firstName': 'firstname', 'lastName': 'lastName', 'roles': ['Group Supervisor']})
user_id = xm_person.get_person('username')['id']
xm_person.modify_person({'id': user_id, 'firstName': 'new_firstname'})
xm_person.get_people_collection()
xm_person.remove_person('username')
```

#### pyxmatters/rest/device.py

```
import xmatters
import logging
logging.basicConfig(filename='log.log',level=10,datefmt='%m-%d-%Y %H:%M:%S',format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_person = xmatters.xMattersPerson(environment)
xm_device = xmatters.xMattersDevice(environment)

log.info("Starting Process")
user_id = xm_person.get_person('username')['id'] # needed for device creation
xm_device.create_device({'name': 'Work Email', 'emailAddress': 'user@xmatters.com', 'deviceType': 'EMAIL', 'owner': user_id})
xm_device.get_devices()
# other options available as well
```

#### pyxmatters/rest/group.py
```
import xmatters
import logging
logging.basicConfig(filename='log.log',level=10,datefmt='%m-%d-%Y %H:%M:%S',format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_group = xmatters.xMattersGroup(environment)

log.info("Starting Process")
group = xm_group.create_group({'targetName': 'Test Group'})
xm_group.modify_group({'id': group['id'], 'status': 'INACTIVE'})
xm_group.get_group('Test Group')
xm_group.get_group_collection()
xm_group.remove_group('Test Group')
```

#### pyxmatters/rest/shift.py

```
import xmatters
import logging
logging.basicConfig(filename='log.log',level=10,datefmt='%m-%d-%Y %H:%M:%S',format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_shift = xmatters.xMattersShift(environment)

log.info("Starting Process")
xm_shift.create_shift('Test Group', {'name': 'Test Shift'})
xm_shift.add_member_to_shift('Test Group', 'Default Shift', 'username')
xm_shift.get_shifts('Test Group')
xm_shift.get_shift('Test Group', 'Default Shift')
xm_shift.delete_shift('Test Group', 'Default Shift')
```

#### pyxmatters/rest/roster.py

```
import xmatters
import logging
logging.basicConfig(filename='log.log',level=10,datefmt='%m-%d-%Y %H:%M:%S',format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_roster = xmatters.xMattersRoster(environment)

log.info("Starting Process")
xm_roster.add_member_to_roster('Test Group', 'username')
xm_roster.get_roster('Test Group')
xm_roster.remove_member_from_roster('Test Group', 'username')
xm_roster.get_roster_collection()
```

#### pyxmatters/rest/site.py

```
import xmatters
import logging
logging.basicConfig(filename='log.log',level=10,datefmt='%m-%d-%Y %H:%M:%S',format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_site = xmatters.xMattersSite(environment)

log.info("Starting Process")
xm_site.create_site({'name': 'New Site', 'timezone': 'US/Eastern', 'language': 'EN', 'country': 'USA'})
site = xm_site.get_site('Default Site')
xm_site.get_sites()
xm_site.modify_site({'id': site['id'], 'timezone': 'US/Pacific'})
```

#### pyxmatters/rest/oncall.py

```
import xmatters
import logging
logging.basicConfig(filename='log.log',level=10,datefmt='%m-%d-%Y %H:%M:%S',format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_on_call = xmatters.xMattersOnCall(environment)
xm_group = xmatters.xMattersGroup(environment)

groups = xm_group.get_group_collection('status=ACTIVE')
log.info("Received Active Groups: " + json.dumps(groups))
print("Number of Active Groups returned: " + str(len(groups)))

for group in groups:
    print("Getting On Call Schedule for Group: " + str(group['targetName']))
    group_on_call = xm_on_call.get_on_call_collection("&groups="+group['targetName'])
    log.info("Received On Call Schedule for Group: " + json.dumps(group_on_call))
```

### pyxmatters/util
This directory contains misc. utilities that provide benefits to users executing ETL processes with pyxmatters.

#### pyxmatters/util/column.py
column.py is a class responsible for reading csv files. The intent of this class is to treat a csv like a sql db.

The core function leveraged in column.py is get_rows, below are the details for the function

```
    columns [Array] (Required): 
        Array of string objects that are to be retrieved from the file i.e.,
        ['targetName', 'roles'] will only return identified headers
        ["*"] will return all columns
    
    select [Set or Dict] (Optional): This is a single SELECT statement
        Pass either a set() i.e. {"targetName"}
        or Pass a dict() i.e. {"targetName": "Application Developers"}
        This will be default only accept the first value passed in either the set or dict
        
    distinct [Boolean] Optional: This field will return duplicate rows for a key if false, if true will
        return every occurrence for a key
        
    delimiter_to_array [String](Optional): delimiter to be used to split a field value to an array, i.e. 
        if ";" provided: ldavid;jseinfeld --> ['ldavid', 'jseinfeld']
```

Save the file below as a dynamic_teams.csv in UTF-8 Encoding:
```
targetName,supervisors,observers,operand,criterionType,field,criterionOperand,value
Dynamic Teams 1,jerry.seinfeld,Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Philadelphia
Dynamic Teams 1,jerry.seinfeld,Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Washington D.C.
Dynamic Teams 2,larry.david;jerry.seinfeld,REST Web Service User;Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Based at Home
Dynamic Teams 2,larry.david;jerry.seinfeld,REST Web Service User;Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Brooklyn
Dynamic Teams 2,larry.david;jerry.seinfeld,REST Web Service User;Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Hoboken
Dynamic Teams 2,larry.david;jerry.seinfeld,REST Web Service User;Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,West Village
```

Execute the below for testing:
```
import xmatters
import logging
logging.basicConfig(filename='log.log',level=10,datefmt='%m-%d-%Y %H:%M:%S',format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

dynamic_teams_file = xmatters.Column("dynamic_teams.csv", "utf-8-sig")

# 1.) Pass: Return specific columns, this should return every occurrence of the targetName
dynamic_teams_data = dynamic_teams_file.get_rows(["targetName"])
log.info(json.dumps(dynamic_teams_data))

# 2.) Pass: Return all columns and delimiter
dynamic_teams_data = dynamic_teams_file.get_rows(["*"], None, None, ";")
log.info(json.dumps(dynamic_teams_data))

# 3.) Passed: Return all columns, this should return every occurrence of the targetName
dynamic_teams_data = dynamic_teams_file.get_rows(["*"], {"targetName"}, False, ";")
log.info(json.dumps(dynamic_teams_data))

# 4.) Passed: Return a distinct list of targetNames
dynamic_teams_data = dynamic_teams_file.get_rows(["*"], {"targetName"}, True, ";")
log.info(json.dumps(dynamic_teams_data))

# 5.) Passed: Should only return a distinct list of the passed key/value
dynamic_teams_data = dynamic_teams_file.get_rows(["*"], {"targetName": "Dynamic Teams 2"}, True, ";")
log.info(json.dumps(dynamic_teams_data))

# 6.) Passed: Should return every occurrence of the passed key/value
dynamic_teams_data = dynamic_teams_file.get_rows(["*"], {"targetName": "Dynamic Teams 2"}, False, ";")
log.info(json.dumps(dynamic_teams_data))
```

#### pyxmatters/util/timecalc.py
timecalc.py is a helper class for displaying start and end durations of a running process
```
import xmatters
import time
time_util = xmatters.TimeCalc()

# time start
start = time_util.get_time_now()
print("Starting Process: " + time_util.format_date_time_now(start))

# sleep for one second
time.sleep(1)

# time end
end = time_util.get_time_now()
print("Process Duration: " + time_util.get_diff(end, start))
```
## Working Projects
For implementation in a working project see: https://github.com/matthewhenry1/integrator_py



## Notes For Contributors

### Uploading
`wheel` and `twine` are required for packaging and uploading:
* `pip3 install wheel`
* `pip3 install twine`

Procedure:
1. Update the version in the setup.py. Increment by 1 and keep existing structure
2. `python3 setup.py sdist bdist_wheel`
3. `twine upload dist/*`

Before updating GitHub:
* For MacOS users: Recursively remove compiled files prior to uploading to GitHub
    * From within src directory (i.e. `/pyxmatters`) execute the following: `find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf`

References:
* https://pypi.org/project/twine/
* https://stackoverflow.com/questions/52016336/how-to-upload-new-versions-of-project-to-pypi-with-twine

### Testing locally
To test locally uninstall the package by:
* `sudo pip3 uninstall pyxmatters`
* add `xmatters` to the local directory in which you want to test and then import `xmatters` as you normally would to begin testing

