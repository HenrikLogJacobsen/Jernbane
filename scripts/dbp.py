import sqlite3
import queries as q
import user_functions as uf

con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()

cursor.execute("DELETE FROM Banestrekning")
cursor.execute("DELETE FROM Delstrekning")
cursor.execute("DELETE FROM Kunde")
cursor.execute("DELETE FROM Kundeordre")
cursor.execute("DELETE FROM Kupe")
cursor.execute("DELETE FROM Operator")
cursor.execute("DELETE FROM PaRute")
cursor.execute("DELETE FROM RutePaStrekning")
cursor.execute("DELETE FROM RutePaUkedag")
cursor.execute("DELETE FROM Seng")
cursor.execute("DELETE FROM SengeBillett")
cursor.execute("DELETE FROM Sittebillett")
cursor.execute("DELETE FROM Stasjon")
cursor.execute("DELETE FROM Stol")
cursor.execute("DELETE FROM Togrute")
cursor.execute("DELETE FROM Vogn")
cursor.execute("DELETE FROM Togruteforekomst")
cursor.execute("DELETE FROM Vognoppsett")



con.commit()

con.close()
