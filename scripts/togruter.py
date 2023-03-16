import sqlite3
import queries as q

con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()


q.db_insert(cursor, "Banestrekning", ['Nordlandsbanen', 'diesel'])
q.db_insert(cursor, "Banestrekning", ['Nordlandsbanen', 'diesel'])




con.commit()

cursor.execute("SELECT * FROM Togrute")

print(cursor.fetchall())


con.close()




