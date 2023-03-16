import sqlite3
import queries as q

con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()


q.db_insert(cursor, "Kunde", ['1', 'Jonas', 'jonas@mail.com', '98057752'])

con.commit()

cursor.execute("SELECT * FROM Banestrekning")

print(cursor.fetchall())


con.close()




