# ts_raw = "datetime.datetime(2020, 01, 28, 1, 1, 3)"
# ts_stripped = ts_raw.replace('datetime.datetime', '').replace(' ','')
# ts_sliced = ts_stripped[1:-1]
# ts = ts_sliced.split(',')
# if len(ts[3]) == 1:
#     ts[3] = '0' + ts[3]
# if len(ts[4]) == 1:
#     ts[4] = '0' + ts[4]
# if len(ts[5]) == 1:
#     ts[5] = '0' + ts[5]
# timestamp = ts[2] + '.' + ts[1] + '.' + ts[0] + ', ' + ts[3] + ':' + ts[4] + ':' + ts[5]
# print(timestamp)
#
#
# strings = 77
# strings_csv = ''
# strings_eng = ''
#
# for number in range(1, strings + 1):
#     if number == strings:
#         strings_csv = strings_csv + str(number)
#     else:
#         strings_csv = strings_csv + str(number) + ','
# if strings_csv == '1':
#     strings_eng = 'String' + ' ' + strings_csv
# else:
#     strings_eng = 'Strings' + ' ' + strings_csv
#
# print(strings_csv)
# print(strings_eng)

city_population = {"New York City": 8550405,
                   "Los Angeles": 3971883,
                   "Toronto": 2731571,
                   "Chicago": 2720546,
                   "Houston": 2296224,
                   "Montreal": 1704694,
                   "Calgary": 1239220,
                   "Vancouver": 631486,
                   "Boston": 667137}

print(city_population.index(667137))