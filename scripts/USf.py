import queries as q
import sqlite3



con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()

cursor.execute("SELECT * FROM Seng")

ans = cursor.fetchall()


print(ans)



