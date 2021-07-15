import sql_queries as sql  # sql_queries.py contains database queries
import fdb  # fdb is a module for interacting with firebird
import os  # operating system functions
from tkinter import *  # tkinter module for GUI setup
from tkinter import ttk, filedialog  # ttk for more GUI widgets and filedialog for opening files
from tkcalendar import Calendar  # tkcalendar for date selection

# GUI frame setup
root = Tk()
root.title("Reporting Service Tool")
root.resizable(False, False)
frame = ttk.Frame(root).grid(row=0, column=0)

# Get previous settings from config.txt and store them in config list
config = []  # 0=db path, 1=reports path, 2=from date, 3=to date
config_file = open('config.txt', 'r')
for line in config_file:
    config.append(line.rstrip('\n'))
config_file.close()


# Parameters
database_path = StringVar(value=config[0])
reports_path = StringVar(value=config[1])
from_date = StringVar(value=config[2])
to_date = StringVar(value=config[3])
systems = {}  # initialise systems dictionary (k = name, v = id number)
strings = {}  # initialise strings dictionary (k = id number, v = number of strings)
reports = ["Discharge Summary", "Discharge Activity", "Discharge Report", "String History", "Alarm History"]


# Sets database path
def set_database_path():
    db_path = filedialog.askopenfilename(filetypes=[("Link database (Link.fdb)", "Link.fdb")])
    database_path.set(db_path)


# Set report path after user browses to it and clicks on it
def set_reports_path():
    rep_path = filedialog.askdirectory()
    database_path.set(rep_path)


# Set date to begin reports (using tkcalendar module)
def set_date_from():
    def apply():
        date = calendar.get_date()
        from_date.set(date)
        window.destroy()

    window = Toplevel(frame)
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

    window = Toplevel(frame)
    calendar = Calendar(window, selectmode='day', locale='en_AU',
                        cursor='hand1', year=2020, month=10, day=30,
                        date_pattern='dd.mm.yyyy')
    calendar.pack(fill="both", expand=True)
    ttk.Button(window, text="Apply To Date", command=apply).pack()


# Sets configuration and stores it in config.txt
def set_config():
    file = open('config.txt', 'w')
    file.write(get_database_path() + '\n')
    file.write(get_reports_path() + '\n')
    file.write(get_from_date() + '\n')
    file.write(get_to_date() + '\n')
    file.close()


# Getters for tkinter variables
def get_database_path():
    return database_path.get()


def get_reports_path():
    return reports_path.get()


def get_from_date():
    return from_date.get()


def get_to_date():
    return to_date.get()


# Connect button, populates system listbox and gets string numbers in background
def connect_to_database():
    systems_unsorted = {}
    """Reset system listbox"""
    systems_listbox.delete(0, END)

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

    for items in dict(sorted(systems.items())):
        systems_listbox.insert(END, items)

    systems_listbox.select_set(0, END)
    reports_listbox.select_set(0, END)

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
    system_names = []  # string name list from systems listbox
    selected_reports = []  # integer item list from reports listbox
    report_names = []  # string name list from reports listbox

    """The below for loops move selected listbox items to lists"""
    for system in systems_listbox.curselection():  # iterates over each system selection
        selected_systems.append(system)  # iterations added as integer items to selected_systems list
    for system in selected_systems:  # iterates over each integer in selected_systems
        system_names.append(systems_listbox.get(system))  # appends string name of systems to system_names
    for rep in reports_listbox.curselection():  # iterates over each report selection
        selected_reports.append(rep)  # iterations added as integer items to selected reports list
    for rep in selected_reports:  # iterates over each integer in selected_reports
        report_names.append(reports_listbox.get(rep))  # appends string name of reports to report_names

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
            if discharge[0] in system_names:  # check if the system is selected in the listbox
                cursor.execute(sql.discharge_report(discharge[0], discharge[2], strings[discharge[2]],
                                                    discharge[3].strftime("%d/%m/%Y %H:%M:%S")))
                connection.commit()

    """Get Discharge Activity Reports"""
    if "Discharge Activity" in report_names:
        for name in system_names:
            cursor.execute(sql.discharge_activity(get_from_date(), get_to_date(), name, systems[name]))
            connection.commit()

    """Get String History Reports"""
    if "String History" in report_names:
        for name in system_names:
            cursor.execute(sql.string_history(get_from_date(), get_to_date(), strings[systems[name]], name,
                                              systems[name]))
            connection.commit()

    """Get Alarm History Reports"""
    if "Alarm History" in report_names:
        for name in system_names:
            cursor.execute(sql.alarm_history(get_from_date(), get_to_date(), name, systems[name]))
            connection.commit()

    connection.close()
    os.startfile(reports_path.get())
    set_config()


def about():
    window = Toplevel(root)
    ttk.Label(window, text='Reporting Service Tool').pack(anchor='center', padx=10, pady=10)
    ttk.Label(window, text='Version 1.0').pack(anchor='center', padx=10)
    ttk.Button(window, text="Close", command=window.destroy).pack(anchor='center', padx=10, pady=10)


def instructions():
    window = Toplevel(frame)
    ttk.Label(window, text="Instructions").pack(anchor='center', padx=10, pady=10)
    ttk.Label(window, text="1. PSReportServer service must be running (starts with Link Client)").pack(anchor=W,
                                                                                                       padx=10)
    ttk.Label(window, text="2. If first time use, check Database and Report paths are correct").pack(anchor=W,
                                                                                                     padx=10)
    ttk.Label(window, text="3. Click Connect to get list of systems").pack(anchor=W, padx=10)
    ttk.Label(window, text="4. Choose 'Systems to Include' in reports").pack(anchor=W, padx=10)
    ttk.Label(window, text="5. Choose the 'From Date' and 'To Date' for the reports").pack(anchor=W, padx=10)
    ttk.Label(window, text="6. Pick the category of 'Reports' to generate").pack(anchor=W, padx=10)
    ttk.Label(window, text="7. Click 'Generate Reports'").pack(anchor=W, padx=10)
    ttk.Label(window, text="8. Reports folder will open and reports will be generated").pack(anchor=W, padx=10)
    ttk.Button(window, text="Close", command=window.destroy).pack(anchor='center', padx=10, pady=10)


# GUI widget setup and grid placement
"""Database path and Connect button"""
ttk.Label(frame, text='Link Database File').grid(column=1, row=0, sticky=E, padx=10)
ttk.Entry(frame, textvariable=database_path, width=60).grid(column=2, row=0, columnspan=4, sticky=(E, W))
ttk.Button(frame, text='...', width=5, command=set_database_path).grid(column=6, row=0, sticky=W)
ttk.Button(frame, text='Connect', command=connect_to_database).grid(column=7, row=0, sticky=W, pady=10)

"""Reports path"""
ttk.Label(frame, text='Link Reports Folder').grid(column=1, row=1, sticky=E, padx=10)
ttk.Entry(frame, textvariable=reports_path, width=60).grid(column=2, row=1, columnspan=4, sticky=(E, W))
ttk.Button(frame, text='...', width=5, command=set_reports_path).grid(column=6, row=1, sticky=W)
ttk.Button(frame, text='Browse', command=lambda: os.startfile(reports_path.get())).grid(column=7,
                                                                                        row=1, sticky=W, pady=5)

"""System listbox"""
ttk.Label(frame, text='Systems to Include').grid(column=1, row=2, sticky=E, padx=10)
systems_scrollbar_x = Scrollbar(frame, orient='horizontal')
systems_scrollbar_x.grid(column=2, row=3, columnspan=6, sticky=(E, W))
systems_scrollbar_y = Scrollbar(frame, orient='vertical')
systems_scrollbar_y.grid(column=8, row=2, sticky=(N, S, W))
systems_listbox = Listbox(frame, selectmode=EXTENDED, exportselection=0, width=60, height=20)
systems_listbox.grid(column=2, row=2, columnspan=6, sticky=(E, W))
systems_listbox.config(xscrollcommand=systems_scrollbar_x.set)
systems_listbox.config(yscrollcommand=systems_scrollbar_y.set)
systems_scrollbar_x.config(command=systems_listbox.xview)
systems_scrollbar_y.config(command=systems_listbox.yview)

"""Report from date"""
ttk.Label(frame, text='From Date').grid(column=1, row=4, sticky=E, padx=10)
ttk.Entry(frame, textvariable=from_date, justify='right', width=20).grid(column=2, row=4, sticky=E)
ttk.Button(frame, text='...', width=5, command=set_date_from).grid(column=3, row=4, sticky=W)

"""Report to date"""
ttk.Label(frame, text='To Date').grid(column=1, row=5, sticky=E, padx=10)
ttk.Entry(frame, text=to_date, justify='right', width=20).grid(column=2, row=5, sticky=E)
ttk.Button(frame, text='...', width=5, command=set_date_to).grid(column=3, row=5, sticky=W)

"""Reports listbox"""
ttk.Label(frame, text='Reports').grid(column=4, row=4, rowspan=2, padx=5, sticky=(N, S, E))
reports_listbox = Listbox(frame, selectmode=EXTENDED, exportselection=0, width=25, height=5)
reports_listbox.grid(column=6, row=4, sticky=(N, E, W), columnspan=2, rowspan=2, pady=10)
for report in reports:
    reports_listbox.insert(END, report)
ttk.Label(frame, text='    ').grid(column=9, row=4)  # white space for aesthetics

"""Generate button"""
ttk.Button(frame, text='Generate Reports', command=generate_reports).grid(column=3, row=8, columnspan=2,
                                                                          pady=10, sticky=W)

"""Menu"""
menubar = Menu(frame)
menu = Menu(menubar, tearoff=0)
menu.add_command(label="Instructions", command=instructions)
menu.add_separator()
menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=menu)
root.config(menu=menubar)

root.mainloop()
