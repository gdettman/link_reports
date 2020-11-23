def system_list():
    query = "select PKEY, C_29_F3 from C_29"
    return query


def string_list():
    query = "select distinct C_12_F1, C_12_F8 from C_12"
    return query


def discharge_list(start, end):
    query = ("select distinct "
             "a.C_29_F3 as Sitename,"
             "a.C_29_F1 as Del,"
             "a.PKEY as Sitenum,"
             #"--,b.C_12_F8 as Strings"
             "c.C_10_F2 as StartDate,"
             "c.C_10_F3 as Mode "
             "from C_29 a join C_12 b on C_12_F1 = a.PKEY "
             "   join C_10 c on C_10_F1 = b.PKEY "
             "where (C_10_F3 = 'D') "
             f"  and (C_10_F2 >= '{start} 00:00:00') "
             f"  and (C_10_F2 < '{end} 23:59.59') "
             "order by 1,2,3,4,5;")
    return query


def discharge_summary(start, end):
    start_slash = start.replace('.', '/')
    end_slash = end.replace('.', '/')
    query = ("INSERT INTO C_47 (DERIVED_, PKEY, C_47_F1, C_47_F2, C_47_F3, C_47_F4, C_47_F5, C_47_F6, C_47_F7, "
             "C_47_F8, C_47_F9, C_47_F10, C_47_F11, C_47_F12, C_47_F13, C_47_F14) VALUES (" + "\n"
             "'47'," + "\n"
             "GEN_ID(GEN_C_47, 1)," + "\n"
             "'ADMIN'," + "\n"
             "'1'," + "\n"
             "'NOW'," + "\n"
             "'0'," + "\n"
             "'30.12.1899 00:00:00'," + "\n"
             f"'Discharge Summary - {start_slash} to {end_slash} - DS'," + "\n"
             "'6'," + "\n"
             f"'{start} 00:00:00'," + "\n"
             f"'{end} 23:59:59'," + "\n"
             "'0'," + "\n"
             "'[Report] " + "\n"
             f"Start={start_slash} " + "\n"
             f"End={end_slash} " + "\n"
             "B1000=0 " + "\n"
             "[DischargeSummaryReport] " + "\n"
             "Temperature type=0 " + "\n"
             "RawDataFormat=No " + "\n"
             "ByString=No " + "\n"
             "IgnoreShort=No" + "\n"
             "'," + "\n"
             "'30.12.1899, 00:00:00'," + "\n"
             "''," + "\n"
             "'');")
    return query


def discharge_activity(start, end, name, id_number):
    start_slash = start.replace('.', '/')
    end_slash = end.replace('.', '/')
    query = ("INSERT INTO C_47 (DERIVED_, PKEY, C_47_F1, C_47_F2, C_47_F3, C_47_F4, C_47_F5, C_47_F6, C_47_F7, "
             "C_47_F8, C_47_F9, C_47_F10, C_47_F11, C_47_F12, C_47_F13, C_47_F14) VALUES (" + "\n"
             "'47'," + "\n"
             "GEN_ID(GEN_C_47, 1)," + "\n"
             "'ADMIN'," + "\n"
             "'1'," + "\n"
             "'NOW'," + "\n"
             "'0'," + "\n"
             "'30.12.1899 00:00:00'," + "\n"
             f"'Discharge Activity - {name} - {start_slash} to {end_slash} - DS'," + "\n" 
             "'7'," + "\n" 
             f"'{start} 00:00:00'," + "\n"
             f"'{end} 23:59:59'," + "\n"
             "'0'," + "\n"
             "'[Report]" + "\n"
             f"Start={start_slash}" + "\n"
             f"End={end_slash}" + "\n"
             f"B1000={id_number}" + "\n"
             "[DischargeActivityReport]" + "\n"
             "Temperature type=0" + "\n"
             "RawDataFormat=No" + "\n"
             "Group=0" + "\n"
             "ByString=No" + "\n"
             "IgnoreShort=No" + "\n"
             "'," + "\n"
             "'30.12.1899, 00:00:00'," + "\n"
             "''," + "\n"
             "'');")
    return query


def discharge_report(name, id, strings, timestamp):
    timestamp_dot = timestamp.replace('/', '.')
    strings_csv = ''
    strings_eng = ''

    for number in range(1, strings + 1):
        if number == strings:
            strings_csv = strings_csv + str(number)
        else:
            strings_csv = strings_csv + str(number) + ','
    if strings_csv == '1':
        strings_eng = 'String' + ' ' + strings_csv
    else:
        strings_eng = 'Strings' + ' ' + strings_csv

    query = ("INSERT INTO C_47 (DERIVED_, PKEY, C_47_F1, C_47_F2, C_47_F3, C_47_F4, C_47_F5, C_47_F6, C_47_F7, "
             "C_47_F8, C_47_F9, C_47_F10, C_47_F11, C_47_F12, C_47_F13, C_47_F14) VALUES (" + "\n"
             "'47'," + "\n"
             "GEN_ID(GEN_C_47, 1)," + "\n"
             "'ADMIN'," + "\n"
             "'1'," + "\n"
             "'NOW'," + "\n"
             "'0'," + "\n"
             "'30.12.1899 00:00:00'," + "\n"
             f"'Discharge - {name} - {strings_eng} - {timestamp_dot} - DR'," + "\n"
             "'1'," + "\n"
             f"'{timestamp_dot}'," + "\n"
             f"'{timestamp_dot}'," + "\n"
             f"'{id}'," + "\n"
             "'[Report] " + "\n"
             f"Start={timestamp} " + "\n"
             f"End={timestamp} " + "\n"
             f"B1000={id} " + "\n"
             "[DischargeReport] " + "\n"
             "Group=0 " + "\n"
             f"MBStrings={strings_csv} " + "\n"
             "ChartAlarms=Yes " + "\n"
             "SortByStrings=Yes " + "\n"
             "ReportingDuration=Maximum " + "\n"
             "AutoScale=No " + "\n"
             "Temperature type=0 " + "\n"
             "RawDataFormat=No " + "\n"
             "PreDischargeDate= " + "\n"
             "Limits enabled=0 " + "\n"
             "MB Voltage Min=0 " + "\n"
             "MB Temperature Max=30000 " + "\n"
             "String Voltage Min=0 " + "\n"
             "String Current Max=0 " + "\n"
             "Ambient Temperature Min=15000 " + "\n"
             "Ambient Temperature Max=30000', " + "\n"
             "'30.12.1899 00:00:00'," + "\n"
             "''," + "\n"
             "'');")
    return query


def string_history(start, end, strings, name, id_number):
    start_slash = start.replace('.', '/')
    end_slash = end.replace('.', '/')

    strings_csv = ''
    strings_eng = ''

    for number in range(1, strings + 1):
        if number == strings:
            strings_csv = strings_csv + str(number)
        else:
            strings_csv = strings_csv + str(number) + ','
    if strings_csv == '1':
        strings_eng = 'String' + ' ' + strings_csv
    else:
        strings_eng = 'Strings' + ' ' + strings_csv

    query = ("INSERT INTO C_47(DERIVED_, PKEY, C_47_F1, C_47_F2, C_47_F3, C_47_F4, C_47_F5, C_47_F6, C_47_F7, " 
            "C_47_F8, C_47_F9, C_47_F10, C_47_F11, C_47_F12, C_47_F13, C_47_F14) VALUES (" + "\n"
            "'47'," + "\n"
            "GEN_ID(GEN_C_47, 1)," + "\n"
            "'ADMIN'," + "\n"
            "'1'," + "\n"
            "'NOW'," + "\n"
            "'0'," + "\n"
            "'30.12.1899 00:00:00'," + "\n"
            f"'String History - {name} - {strings_eng} - {start_slash} to {end_slash} - SH'," + "\n"
            "'2'," + "\n"
            f"'{start} 00:00:00'," + "\n"
            f"'{end} 23:59:59'," + "\n"
            f"'{id_number}'," + "\n"
            "'[Report]" + "\n"
            f"Start = {start_slash}" + "\n"
            f"End = {end_slash}" + "\n"
            f"B1000 = {id_number}" + "\n"
            "[StrHistoryReport]" + "\n"
            "MBDetail = Yes" + "\n"
            f"MBStrings = {strings_csv}" + "\n"
            "AlarmDetail = No" + "\n"
            "FilterDischarge = No" + "\n"
            "TotalHistory = No" + "\n"
            "Temperature" + "\n"
            "type = 0" + "\n"
            "RawDataFormat = No" + "\n"
            "MinMaxRawData = No" + "\n"
            "Limit1 = 10" + "\n"
            "Limit2 = 30" + "\n"
            "'," + "\n"
            "'30.12.1899 00:00:00'," + "\n"
            "''," + "\n"
            "'');")
    return query