import sqlite3
con = sqlite3.connect('ramazon.sqlite')
cur = con.cursor()
from datetime import datetime,timedelta


def kun_bugun():
    today=str(datetime.now().date())
    cur.execute('select * from ramadan_calendar where r_date=? ',(today,))
    info_1=cur.fetchone()
    print(info_1)
    info_0=str(info_1)
    if info_0=='None':
        info='false'
    else:
        info='true'
    return info

# print(kun_bugun())
# vaqt =str(kun(today))
# print(vaqt)
