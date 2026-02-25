import sqlite3

conn = sqlite3.connect('database/data.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_schema WHERE type='table'")
tables = cursor.fetchall()



tables_dict = {}
for i in tables:
    if i[0] != 'sqlite_sequence':
        cursor.execute(f"PRAGMA table_info({i[0]})")
        columns = cursor.fetchall()
        tables_dict[i[0]]=[]
        for col in columns:
            tables_dict[i[0]].append(col[1])

TAB = ''
for key,val in tables_dict.items():
    TAB += key+f'{tuple(val)}'+'\n'
print(TAB)
conn.close()