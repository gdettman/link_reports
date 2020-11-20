

def list_of_discharges(start, end):
    query = ("select distinct "
             "a.C_29_F3 as Sitename,"
             "a.C_29_F1 as Del,"
             "a.PKEY as Sitenum,"
             "c.C_10_F2 as StartDate,"
             "c.C_10_F3 as Mode "
             "from C_29 a join C_12 b on C_12_F1 = a.PKEY "
             "   join C_10 c on C_10_F1 = b.PKEY "
             "where (C_10_F3 = 'D') "
             f"  and (C_10_F2 >= '{start} 00:00:00') "
             f"  and (C_10_F2 < '{end} 23:59.59') "
             "order by 1,2,3,4,5;")
    return query


def discharge_summary_report(start, end):
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
             f"'Discharge Summary - {start} to {end} - DS'," + "\n"
             "'6'," + "\n"
             f"'{start} 00:00:00'," + "\n"
             f"'{end} 23:59:59'," + "\n"
             f"'0'," + "\n"
             f"'[Report] " + "\n"
             f"Start={start_slash} " + "\n"
             f"End={end_slash} " + "\n"
             f"B1000=0 " + "\n"
             f"[DischargeSummaryReport] " + "\n"
             "Temperature type=0 " + "\n"
             "RawDataFormat=No " + "\n"
             "ByString=No " + "\n"
             "IgnoreShort=No" + "\n"
             "'," + "\n"
             "'30.12.1899, 00:00:00'," + "\n"
             "''," + "\n"
             "'');")
    print(query)
    return query
