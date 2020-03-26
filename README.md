# pyxmatters
The pyxmatters package provides a rest api interface with xMatters. There are also file reading capabilities to assist with synchronizing data.

## Install pyxmatters
Navigate to the cmd and enter:
* `pip3 install pyxmatters`

## For Upgrades of pyxmatters
Navigate to the cmd and enter:
* `sudo pip3 install --upgrade --force-reinstall pyxmatters`

Reference:
* https://stackoverflow.com/questions/47071256/how-to-update-upgrade-a-package-using-pip

## Overview of the pyxmatters package

### /pyxmatters/rest
This directory provides user, device, group, and site rest api capabilities.

### /pyxmatters/util
This directory contains misc. utilities that provide benefits to users executing ETL processes with pyxmatters.

#### /pyxmatters/util/column.py
column.py is a class responsible for reading csv files. The intent of this class is to treat a csv like a sql db.

#### /pyxmatters/util/timecalc.py
timecalc.py is a helper class for displaying start and end durations of a running process
```
import xmatters
import time
time_util = xmatters.TimeCalc()

# time start
start = time_util.getTimeNow()
print("Starting Process: " + time_util.formatDateTimeNow(start))

# sleep for one second
time.sleep(1)

# time end
end = time_util.getTimeNow()
print("Process Duration: " + time_util.getDiff(end, start))
```

## Working Projects
For implementation in a working project see: https://github.com/matthewhenry1/integrator_py

## Notes on managing the package

### Uploading
`wheel` and `twine` are required for packaging and uploading:
* `pip3 install wheel`
* `pip3 install twine`

Procedure:
1. Update the version in the setup.py. Increment by 1 and keep existing structure
2. `python3 setup.py sdist bdist_wheel`
3. `twine upload dist/*`

References:
* https://pypi.org/project/twine/
* https://stackoverflow.com/questions/52016336/how-to-upload-new-versions-of-project-to-pypi-with-twine

### Testing locally
To test locally uninstall the package by:
* `sudo pip3 uninstall pyxmatters`
* add `pyxmatters` to the local directory in which you want to test and then import `pyxmatters` as you normally would
* begin testing

## Miscellaneous Notes
* For MacOS users: Recursively remove compiled files prior to uploading to GitHub
    * From within src directory (i.e. `/xm-integrator-py/src`) execute the following: `find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf`
