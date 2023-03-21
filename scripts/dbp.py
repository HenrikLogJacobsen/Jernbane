import sqlite3
import queries as q
import user_functions as uf

con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()

## opg c
# cursor.execute("SELECT RuteID, Ukedag FROM RutePaUkedag NATURAL JOIN PaRute WHERE StasjonNavn=='Mosjøen' AND Ukedag=='lørdag'") ## tolk oppgaven, hvis du vil ha alle hverdager så fjerne AND... ellers behold sån det e nå


# con.commit()

# print(cursor.fetchall())

## opg d

## finner alle ruter som går innom en gitt stasjon etter et gitt klokkeslett en gitt dagen og dagen etter 
uf.find_route(cursor, 'Fauske', 'Bodø', '06:00', 'tirsdag')



con.commit()

for el in cursor.fetchall() : 
    print(el)

## opg e
#uf.create_user(cursor, '10', 'Henrik', 'henrik@mail.com', '1939394949')

## opg f
 


## opg g
cursor.execute(f""" """) 

con.commit()

print(cursor.fetchall())




con.close()