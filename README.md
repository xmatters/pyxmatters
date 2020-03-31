# pyxmatters
pyxmatters is a python3 sdk that provides a RESTful interface with xMatters. Additionally there are capabilities to interface with csv files.

## Install, Upgrades, and use of pyxmatters
For Production use it is **strongly** recommended to download the pyxmatters package locally from GitHub, specifically the `xmatters` directory, and set the `xmatters` directory alongside the script leveraging it. For use locally, just enter `import xmatters` at the top of the calling script as documented in the steps below. This is import is the same procedure as if the package was downloaded using pip. Also, this SDK is a work in progress, not all REST API's are wrapped, so there is additional value in having a local copy to modify as needed. 

For installing locally with the understanding the package will change and could break your script, follow the steps below:

To Install via pip, navigate to the terminal and enter:
* `pip3 install pyxmatters`

To Upgrade via pip, navigate to terminal and enter:
* `sudo pip3 install --upgrade --force-reinstall pyxmatters`

## Working Projects
For implementation in a working project see: https://github.com/matthewhenry1/integrator_py

## Overview of the pyxmatters package

### pyxmatters/rest
This directory provides user, device, group, and site rest api capabilities.

#### Quick Notes on URL Filters in Methods
* Check the url filter string in the signature to determine the proper use of `?` or `&`
* For any methods that include `collections` i.e. `xMattersPerson.get_person_collection`, `xMattersGroup.get_group_collection`, and `_xMattersRoster.get_roster_collection` by default offset and limit will be stripped. Only `&` is supported. So `&status=ACTIVE` or `status=ACTIVE` will work.
* Lastly, by default anything that will be leveraged in a URL will be auto encoded, this applies to targetNames, id's, and the aforementioned filters. So for `xMattersPerson.get_person_collection` the following `embed=roles&roles=Standard User` is fine to pass to as this will be handled automatically.

#### pyxmatters/rest/person.py
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersPerson`. Below are the methods available:
* **get_person**: Accepts the username or user id as well as an optional url filter string i.e. `?embed=roles,supervisors`
* **get_people**: Accepts an optional url filter string, i.e. `?embed=roles,devices&offset=0&limit=1000`
* **create_person**: Requires the json object to create the xMatters record as documented on the xMatters REST API
* **modify_person**: Requires the json object to create the xMatters record as documented on the xMatters REST API
* **remove_person**: Requires the users id 
* **get_people_collection**: A single threaded process to return all users from an instance, there is no limit on what is returned, the process will loop for all records requested. So if there are 60k records in the instance, all records will be returned. To refine the search this function also accepts an optional url filter string, i.e. `&embed=roles&roles=Standard User`

Script Example:
```buildoutcfg
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
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersDevice`. Below are the methods available:
* **get_device**: Accepts the device id as well as an optional url filter string i.e. `?embed=timeframes`
* **get_devices**: Accepts an optional url filter string, i.e. `?embed=timeframes`
* **create_device**: Requires the json object to create the xMatters record as documented on the xMatters REST API
* **modify_device**: Requires the json object to create the xMatters record as documented on the xMatters REST API
* **remove_device**: Requires the device id 

**Script Example:**
```buildoutcfg
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
```

#### pyxmatters/rest/group.py
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersGroup`. Below are the methods available:
* **get_group**: Accepts the group name or group id as well as an optional url filter string i.e. `?embed=supervisors`
* **get_groups**: Accepts an optional url filter string, i.e. `?offset=0&limit=1000`
* **create_group**: Requires the json object to create the xMatters record as documented on the xMatters REST API
* **modify_group**: Requires the json object to create the xMatters record as documented on the xMatters REST API
* **remove_group**: Requires the group id 
* **get_group_collection**: A single threaded process to return all records from an instance, there is no limit on what is returned, the process will loop for all records requested. So if there are 60k records in the instance, all records will be returned. To refine the search this function also accepts an optional url filter string, i.e. `status=ACTIVE`

**Script Example:**
```buildoutcfg
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
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersShift`. Below are the methods available:
* **add_member_to_shift**: Requires the group name or group id, shift name or shift id, and the members name or id
* **get_shift**: Requires the group name or group id and shift name or shift id
* **get_shifts**: RRequires the group name
* **create_shift**: Requires the json object to create the xMatters record as documented on the xMatters REST API
* **delete_shift**: Requires the group name or group id and shift name or shift id

**Script Example:**
```buildoutcfg
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
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersRoster`. Below are the methods available:
* **add_member_to_roster**: Requires the the group name or group id and member name or member id
* **remove_member_from_roster**: Requires the the group name or group id and member name or member id
* **get_roster**: Requires the the group name or group id and optionally accepts a url filter string `&offset=0&limit=1000`
* **get_roster_collection**: Requires the group name or group id

**Script Example:**
```buildoutcfg
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
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersSite`. Below are the methods available:
* **get_site**: Requires the the site name or site id
* **create_site**: Requires the json object to create the xMatters record as documented on the xMatters REST API
* **get_sites**: Returns the first 1000 sites
* **modify_site**: Requires the json object to create the xMatters record as documented on the xMatters REST API
```buildoutcfg
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
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersOnCall`. Below are the methods available:
* **get_on_call_collection**: Accepts a url filter string. By default this function will return all members associated, it will paginate through all shifts and will return all members even if 100. By design this function was built to take care of all processing and paginating for you.

**Script Example:**
```buildoutcfg
import xmatters
import logging
import json
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

#### pyxmatters/rest/collection.py
Below is an example of leveraging the `xMattersCollection`. This python module is a powerful tool to be used increase throughput when executing updates in xMatters. This process was built only for Create, Modify, and Deletion methods. Getter methods should leverage the aforementioned collection methods that are found in the respective moduldes.

The value of this collection is that it provides the ability to include threading or concurrency. Below is an example of using it. The collection module itself is very dynamic, it will always require:
```buildoutcfg
import xmatters
environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_collection = xmatters.xMattersCollection(environment)
max_thread_count = 5

xm_collection.create_collection(INSERT_METHOD_NAME, ARRAY_OF_DATA, max_thread_count)
```
Where in the above **INSERT_METHOD_NAME** is the associated Create, Update, or Delete method. Where **ARRAY_OF_DATA** is the associated data to send to the function.

The **ARRAY_OF_DATA** must match the signature of the method being called, so for instance, since `xMattersGroup.create_group` accepts a parameter named `data`, **ARRAY_OF_DATA** in this case must look like to match the method signature:
```buildoutcfg
[{"data":{"targetName": "groupname_1"}}, {"data":{"targetName": "groupname_2"}}, {"data":{"targetName": "groupname_3"}}]
```

In another scenario, since `xMattersShift.add_member_to_shift` accepts 3 parameters named `group_id`, `shift_id`, and `member_id`, **ARRAY_OF_DATA** in this case must look like to match the method signature:
```buildoutcfg
[{"group_id": "groupname_1", "shift_id": "Default Shift", "member_id": "username_1"}, {"group_id": "groupname_1", "shift_id": "Default Shift", "member_id": "username_2"}, {"group_id": "groupname_1", "shift_id": "Default Shift", "member_id": "username_3"}]
```

**Script Example:**
```buildoutcfg
import xmatters
import logging
import json

logging.basicConfig(filename="log.log",level=10,datefmt="%m-%d-%Y %H:%M:%S",format="%(asctime)s %(name)s %(levelname)s: %(message)s")
log = logging.getLogger(__name__)

environment = xmatters.xMattersAPI("https://<instance>.xmatters.com", "rest_username", "rest_password")
xm_collection = xmatters.xMattersCollection(environment)
max_thread_count = 5

# Example person thread creation
xm_person = xmatters.xMattersPerson(environment)

person_data = []
for x in range(10):
    person_data.append({"data":{"targetName": "username_"+str(x), "firstName": "username_"+str(x), "lastName": "username_"+str(x), "roles": ["Group Supervisor"]}})
person_create_response = xm_collection.create_collection(xm_person.create_person, person_data, max_thread_count)
log.info("Success Response: "+json.dumps(person_create_response["response"]))
log.info("Error Response: " + json.dumps(person_create_response["errors"]))

# Example group thread creation
xm_group = xmatters.xMattersGroup(environment)

group_data = []
for x in range(10):
    group_data.append({"data":{"targetName": "groupname_"+str(x)}})
group_create_response = xm_collection.create_collection(xm_group.create_group, group_data, max_thread_count)
log.info("Success Response: "+json.dumps(group_create_response["response"]))
log.info("Error Response: " + json.dumps(group_create_response["errors"]))


# Example of add member thread
xm_shift = xmatters.xMattersShift(environment)
member_data = []
for x in range(10):
    member_data.append({"group_id": "groupname_"+str(x), "shift_id": "Default Shift", "member_id": "username_"+str(x)})
member_create_response = xm_collection.create_collection(xm_shift.add_member_to_shift, member_data, max_thread_count)
log.info("Success Response: "+json.dumps(member_create_response["response"]))
log.info("Error Response: " + json.dumps(member_create_response["errors"]))

# uncomment below to delete execution from above
# remove_user_data = []
# remove_group_data = []
# for x in range(10):
#     remove_user_data.append({"person_id":"username_"+str(x)})
#     remove_group_data.append({"group_id":"groupname_"+str(x)})
# person_remove_response = xm_collection.create_collection(xm_person.remove_person, remove_user_data, 5)
# group_remove_response = xm_collection.create_collection(xm_group.remove_group, remove_group_data, 5)

```

#### pyxmatters/rest/dynamic_teams.py
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersDynamicTeams`. Below are the methods available:
* **create_dynamic_team**: Requires the json object to create the xMatters record as documented on the xMatters REST API

#### pyxmatters/rest/plans.py
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersPlans`. Below are the methods available:
* **get_plan**: Requires the plan id and accepts an optional url filter string

#### pyxmatters/rest/libraries.py
For specific method signature detail see the file documented above for specifics.

Below is an example of interfacing with `xMattersLibraries`. Below are the methods available:
* **get_libraries**: Requires the plan id and accepts an optional url filter string

### pyxmatters/util
This directory contains misc. utilities that provide benefits to users executing ETL processes with pyxmatters.

#### pyxmatters/util/column.py
column.py is a class responsible for reading csv files. The intent of this class is to treat a csv like a sql db.

The core function leveraged in column.py is get_rows, below are the details for the function

```
    Method: def get_rows(self, columns, select=None, distinct=None, delimiter_to_array=None):

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
```buildoutcfg
targetName,supervisors,observers,operand,criterionType,field,criterionOperand,value
Dynamic Teams 1,jerry.seinfeld,Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Philadelphia
Dynamic Teams 1,jerry.seinfeld,Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Washington D.C.
Dynamic Teams 2,larry.david;jerry.seinfeld,REST Web Service User;Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Based at Home
Dynamic Teams 2,larry.david;jerry.seinfeld,REST Web Service User;Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Brooklyn
Dynamic Teams 2,larry.david;jerry.seinfeld,REST Web Service User;Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,Hoboken
Dynamic Teams 2,larry.david;jerry.seinfeld,REST Web Service User;Company Supervisor,OR,CUSTOM_FIELD,City,EQUALS,West Village
```

Execute the below for testing:
```buildoutcfg
import xmatters
import logging
import json
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
```buildoutcfg
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

## Notes For Contributors

### Variables, Methods, Classes, and File Names
* Variables: should always be lower case, separated by `_` Do not use camel casing.
* Methods: should always be lower case, separated by `_` and do not use camel casing.
* Classes: PyCharm and Python oriented editors will always bark at the `xMatters` prefix, but keep consistent with the standard of `xMatters<purpose>` i.e. `xMattersPerson`
* Keep consistent with short and brief file names, all lower case, separated by `_` and do not use camel casing.

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

### Testing locally
To test locally uninstall the package by:
* `sudo pip3 uninstall pyxmatters`
* add `xmatters` to the local directory in which you want to test and then import `xmatters` as you normally would to begin testing

