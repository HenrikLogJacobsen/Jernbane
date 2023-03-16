import sqlite3
import queries as q

con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()

q.db_insert(cursor, "Banestrekning", ['jonasBanen', 'Diesel'])

con.commit()

cursor.execute("SELECT * FROM Banestrekning")

print(cursor.fetchall())


con.close()




