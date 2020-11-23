import sql_queries as sql                   # sql_queries.py contains database queries
import fdb                                  # fdb is a module for interacting with firebird
import os                                   # operating system functions
import time                                 # for setting wait delays
from tkinter import *                       # tkinter module for GUI setup
from tkinter import ttk, filedialog         # ttk for more GUI widgets and filedialog for opening files
from tkcalendar import Calendar             # tkcalendar for date selection 

# GUI frame setup
root = Tk()
root.title("Reporting Service Tool")
root.resizable(False, False)

# Parameters
database_path = StringVar(value=            # initialise default database path value
                "C:/Program Files (x86)/PowerShield/Link Server/Database/Link.fdb")
from_date = StringVar(value="01.10.2020")   # initialise default from date
to_date = StringVar(value="30.10.2020")     # initialise default to date
systems = {}                                # initialise systems dictionary
strings = {}                                # initialise strings dictionary
reports = ["Discharge Summary",             # report listbox values
           "Discharge Activity",            
           "Discharge Report", 
           "String History"]


# Set database path after user browses to it and clicks on it
def set_database_path():
        path = filedialog.askopenfilename(filetypes=[("Link database (Link.fdb)", "Link.fdb")])
        database_path.set(path)


# Set date to begin reports (using tkcalendar module)
def set_date_from():
    def apply():
        date = calendar.get_date()
        from_date.set(date)
        window.destroy()

    window = Toplevel(root)
    calendar = Calendar(window, selectmode='day', locale='en_AU',
                        cursor='hand1', year=2020, month=10, day=1,
                        date_pattern='dd.mm.yyyy')
    calendar.pack(fill="both", expand=True)
    ttk.Button(window, text="Apply From Date", command=apply).pack()


# Set date to end reports (using tkcalendar module)
def set_date_to():
    def apply():
        date = calendar.get_date()
        to_date.set(date)
        window.destroy()

    window = Toplevel(root)
    calendar = Calendar(window, selectmode='day', locale='en_AU',
                        cursor='hand1', year=2020, month=10, day=30,
                        date_pattern='dd.mm.yyyy')
    calendar.pack(fill="both", expand=True)
    ttk.Button(window, text="Apply To Date", command=apply).pack()


# Getters for tkinter variables
def get_database_path(*args):
    return database_path.get()


def get_from_date(*args):
    return from_date.get()


def get_to_date(*args):
    return to_date.get()


# Connect button, populates system listbox and gets string numbers in background
def connect_to_database():
    """Connect to database with fdb module, instantiate cursor"""
    connection = fdb.connect(
        host='127.0.0.1', database=get_database_path(),
        user='sysdba', password='masterkey')
    cursor = connection.cursor()

    """Get system names, store in systems dictionary"""
    cursor.execute(sql.system_list())
    system_list = cursor.fetchall()
    for system in system_list:
        systems[system[1]] = system[0]
    for items in systems.keys():
        systems_listbox.insert(END, items)
    systems_listbox.select_set(0,END)
    reports_listbox.select_set(0,END)

    """Get number of strings, store in strings dictionary"""
    cursor.execute(sql.string_list())
    string_list = cursor.fetchall()
    for id_number in string_list:
        if id_number[0] not in strings:
            strings[id_number[0]] = id_number[1]
        elif id_number[0] in strings:
            if id_number[1] > strings[id_number[0]]:
                strings[id_number[0]] = id_number[1]

    """close fdb connection"""
    connection.close()

# Generate reports on Generate button click 
def generate_reports():
    selected_systems = []  # integer item list from systems listbox
    system_names = []      # string name list from systems listbox
    selected_reports = []  # integer item list from reports listbox
    report_names = []      # string name list from reports listbox

    """The below for loops move selected listbox items to lists"""
    for system in systems_listbox.curselection():           # iterates over each system selection         
        selected_systems.append(system)                     # iterations added as integer items to selected_systems list
    for system in selected_systems:                         # iterates over each integer in selected_systems  
        system_names.append(systems_listbox.get(system))    # appends string name of systems to system_names  
    for rep in reports_listbox.curselection():              # iterates over each report selection
        selected_reports.append(rep)                        # iterations added as integer items to selected reports list
    for rep in selected_reports:                            # iterates over each integer in selected_reports
        report_names.append(reports_listbox.get(rep))       # appends string name of reports to report_names

    """Connect to database with fdb module, instantiate cursor"""
    connection = fdb.connect(
        host='127.0.0.1', database=get_database_path(),
        user='sysdba', password='masterkey')
    cursor = connection.cursor()

    """Get Discharge Summary Report"""
    if "Discharge Summary" in report_names:
        cursor.execute(sql.discharge_summary(get_from_date(), get_to_date()))
        connection.commit()

    """Get Discharge Reports"""
    if "Discharge Report" in report_names:
        cursor.execute(sql.discharge_list(get_from_date(), get_to_date()))
        discharge_list = cursor.fetchall()
        for discharge in discharge_list:
            if discharge[0] in system_names:    # check if the system is selected in the listbox
                cursor.execute(sql.discharge_report(discharge[0], discharge[2], strings[discharge[2]], discharge[3].strftime("%d/%m/%Y %H:%M:%S")))
                connection.commit()

    """Get Discharge Activity Reports"""
    if "Discharge Activity" in report_names:
        for name in system_names:
            cursor.execute(sql.discharge_activity(get_from_date(), get_to_date(), name, systems[name]))
            connection.commit()

    """Get String History Reports"""
    if "String History" in report_names:
        for name in system_names:
            cursor.execute(sql.string_history(get_from_date(), get_to_date(), strings[systems[name]], name, systems[name]))
            connection.commit()

    connection.close()
    time.sleep(3)
    os.startfile("C:/Program Files (x86)/PowerShield/Link Server/Reports/")


# GUI widget setup and grid placement
"""Database path and Connect button"""
ttk.Label(root, text='Link Database Location').grid(column=1, row=1, sticky=E, padx=10)
ttk.Entry(root, textvariable=database_path).grid(column=2, row=1, columnspan=4, sticky=(E,W))
ttk.Button(root, text='...', width=5, command=set_database_path).grid(column=6, row=1, sticky=W)
ttk.Button(root, text='Connect', command=connect_to_database).grid(column=7, row=1, sticky=W, pady=20)

"""System listbox"""
ttk.Label(root, text='Systems to Include').grid(column=1, row=2, sticky=E, padx=10)
systems_scrollbar_x = Scrollbar(root, orient='horizontal')
systems_scrollbar_x.grid(column=2, row=3, columnspan=6, sticky=(E, W))
systems_scrollbar_y = Scrollbar(root, orient='vertical')
systems_scrollbar_y.grid(column=8, row=2, sticky=(N, S, W))
systems_listbox = Listbox(root, selectmode=EXTENDED, exportselection=0, width=60, height=20)
systems_listbox.grid(column=2, row=2, columnspan=6, sticky=(E,W))
systems_listbox.config(xscrollcommand=systems_scrollbar_x.set)
systems_listbox.config(yscrollcommand=systems_scrollbar_y.set)
systems_scrollbar_x.config(command=systems_listbox.xview)
systems_scrollbar_y.config(command=systems_listbox.yview)

"""Report from date"""
ttk.Label(root, text='From Date').grid(column=1, row=4, sticky=E, padx=10)
ttk.Entry(root, textvariable=from_date, justify='right', width=10).grid(column=2, row=4, sticky=E)
ttk.Button(root, text='...', width=5, command=set_date_from).grid(column=3, row=4, sticky=W)

"""Report to date"""
ttk.Label(root, text='To Date').grid(column=1, row=5, sticky=E, padx=10)
ttk.Entry(root, text=to_date, justify='right', width=10).grid(column=2, row=5, sticky=E)
ttk.Button(root, text='...', width=5, command=set_date_to).grid(column=3, row=5, sticky=W)

"""Reports listbox"""
ttk.Label(root, text='Reports').grid(column=4, row=4, rowspan=2, padx=5, sticky=(N, S, E))
reports_listbox = Listbox(root, selectmode=EXTENDED, exportselection=0, width=20, height=4)
reports_listbox.grid(column=6, row=4, sticky=(N, E, W), columnspan=2, rowspan=2, pady=10)
for report in reports:
    reports_listbox.insert(END, report)
ttk.Label(root, text='    ').grid(column=9, row=4) #white space for aesthetics

"""Generate button"""
ttk.Button(root, text='Generate Reports', command=generate_reports).grid(column=3, row=7, columnspan=2, pady=10, sticky=W)

root.mainloop()