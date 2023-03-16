import sqlite3
import queries as q

con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()

q.db_insert(cursor, "Banestrekning", ['Nordlandsbanen', 'diesel'])

q.db_insert(cursor, "Operator", ['SJ'])


q.db_insert(cursor, "Stasjon", ['Bodø', '4.1'])
q.db_insert(cursor, "Stasjon", ['Fauske', '34.0'])
q.db_insert(cursor, "Stasjon", ['Mo i Rana', '3.5'])
q.db_insert(cursor, "Stasjon", ['Mosjøen', '6.8'])
q.db_insert(cursor, "Stasjon", ['Steinkjer', '3.6'])
q.db_insert(cursor, "Stasjon", ['Trondheim S', '5.1'])

q.db_insert(cursor, "Delstrekning", ['Bodø', 'Fauske' , '60', '1', 'Nordlandsbanen'])

q.db_insert(cursor, "Delstrekning", ['Fauske', 'Mo i Rana' , '170', '1', 'Nordlandsbanen'])

q.db_insert(cursor, "Delstrekning", ['Mo i Rana', 'Mosjøen' , '90', '1', 'Nordlandsbanen'])

q.db_insert(cursor, "Delstrekning", ['Mosjøen', 'Steinkjer' , '280', '1', 'Nordlandsbanen'])

q.db_insert(cursor, "Delstrekning", ['Steinkjer', 'Trondheim' , '120', '0', 'Nordlandsbanen'])




con.commit()

cursor.execute("SELECT * FROM Banestrekning")
cursor.execute("SELECT * FROM Stasjon")
cursor.execute("SELECT * FROM Delstrekning")

print(cursor.fetchall())


con.close()




