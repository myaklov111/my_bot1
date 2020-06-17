import sqlite as sql
import func

sql.unit_db(force=True)


t='7 июня 13:53'
s=func.str_to_date(t)
print(s)

