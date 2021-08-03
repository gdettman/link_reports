# Reporting Service Tool

This is a script with GUI that generates reports from Link software without needing to manually do it from within Link, the purpose is to generate reports in bulk efficiently.

# Requirements

1. Link 4.x, available from powershield.com<br /> 
2. Python 3.x, available from python.org<br /> 
3. fdb (see installation instructions below, this is a library for Firebird database interface)<br /> 
4. tkcalendar (see installation instructions below, this is a library for a Calendar interface)<br /> 


# Installation

1. Copy main.py, sql_queries.py, config.txt & ignore.txt to the same folder.
2. After Python is installed, you may need to reboot to get the Python installer package (pip) working, then from the commandline execute:<br />
```pip install fdb``` <br />
```pip install tkcalendar``` <br />
The above downloads the required external libraries to run the script.

# Configuration

<i>config.txt</i> contains the default Link database path on line 1, the default Link reports path on Line 2, the most recent <i>from date</i> on Line 3, and the most recent <i>to date</i> on Line 4.<br /><br />
<i>ignore.txt</i> contains a list of system names to ignore, one per line.<br /><br />

# Operation

1. Ensure Link is running and all services are running (from Help>Admin Utility>Services menu in Link)<br />
2. The script can be run by executing main.py from the commandline, eg. ```py main.py``` and this should open the GUI.<br />
3. Change the Link Database File and Link Reports Folder paths if these appear inaccurate otherwise skip to 3.<br />
4. Click Connect at the top right, this will then list all the Systems from within the database.<br />
5. Choose a "From Date" and click Apply.<br />
6. Choose a "To Date" and click Apply. <br />
7. Click the type of Reports to include, hold Control and click on each type or click in the box and press Control-A to select all.<br />
8. Click Generate Reports, this will open the reports folder location and begin generating reports, this may take a while depending on how many reports there are to generate.<br />
