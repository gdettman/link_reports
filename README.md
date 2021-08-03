# link_reports

This is a script with GUI that generates reports from Link software without needing to manually do it from within Link, the purpose is to generate reports in bulk efficiently.

# External Dependencies

Link 4.x with all services running<br /> 
Python 3.x <br /> 
fdb (Python library for Firebird database interface)<br /> 
tkcalendar (Python library for Calendar interface)<br /> 

# Internal Dependencies

The minimum files needed to run include main.py (the main script), sql_queries.py (script containing sql queries), config.txt (configuration file) & ignore.txt (system names to ignore).

# Configuration

<i>config.txt</i> contains the default Link database path on line 1, the default Link reports path on Line 2, the most recent from date on Line 3, and the most recent to date on Line 4.<br /><br />
<i>ignore.txt</i> contains a list of system names to ignore, one per line.<br /><br />

# Operation

1. The script can be run by executing main.py from the commandline, eg. "py main.py" and this should open the GUI.<br />
2. Change the Link Database File and Link Reports Folder paths if these appear inaccurate otherwise skip to 3.<br />
3. Click Connect at the top right, this will then list all the Systems from within the database.<br />
4. Choose a "From Date" and click Apply.<br />
5. Choose a "To Date" and click Apply. <br />
6. Click the type of Reports to include, hold Control and click on each type or click in the box and press Control-A to select all.<br />
7. Click Generate Reports, this will open the reports folder location and begin generating reports, this may take a while depending on how many reports there are to generate.<br />
