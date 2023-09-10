import sqlite3
import queries as q
from vogn import sjSittevogn1, sjSovevogn1
from rute import routeWholeWeek, routeMonToFri
con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()

#Hovedrettning er sørover

#Dagtog fra Trondheim til Bodø
sjSittevogn1(cursor, 1)
sjSittevogn1(cursor, 2)

q.db_insert(cursor, "VognOppsett", ['1', '1', '1'])
q.db_insert(cursor, "VognOppsett", ['2', '1', '2'])

q.db_insert(cursor, "Togrute", ['1', 'SJ', "0", 'Trondheim S', 'Bodø'])



# sjSittevogn1(cursor, 3)
# sjSovevogn1(cursor, 1)#stasjoner på ruten 
q.db_insert(cursor, "PaRute", ['Trondheim S', '1', '07:49', '07:49'])
q.db_insert(cursor, "PaRute", ['Steinkjer', '1', '09:51', '09:51'])
q.db_insert(cursor, "PaRute", ['Mosjøen', '1', '13:20', '13:20'])
q.db_insert(cursor, "PaRute", ['Mo i Rana', '1', '14:31', '14:31'])
q.db_insert(cursor, "PaRute", ['Fauske', '1', '16:49', '16:49'])
q.db_insert(cursor, "PaRute", ['Bodø', '1', '17:34', '17:34'])

q.db_insert(cursor, "RutePaUkedag", ['1', 'mandag'])
q.db_insert(cursor, "RutePaUkedag", ['1', 'tirsdag'])
q.db_insert(cursor, "RutePaUkedag", ['1', 'onsdag'])
q.db_insert(cursor, "RutePaUkedag", ['1', 'torsdag'])
q.db_insert(cursor, "RutePaUkedag", ['1', 'fredag'])


q.db_insert(cursor, "RutePaStrekning", ['1', 'Trondheim S', 'Steinkjer'])
q.db_insert(cursor, "RutePaStrekning", ['1', 'Steinkjer', 'Mosjøen'])
q.db_insert(cursor, "RutePaStrekning", ['1', 'Mosjøen', 'Mo i Rana'])
q.db_insert(cursor, "RutePaStrekning", ['1', 'Mo i Rana', 'Fauske'])
q.db_insert(cursor, "RutePaStrekning", ['1', 'Fauske', 'Bodø'])

q.db_insert(cursor, "Togruteforekomst", ['1', '03-04-2023', '1'])
q.db_insert(cursor, "Togruteforekomst", ['2', '04-04-2023', '1'])






#Nattog fra Trondheim til Bodø

sjSittevogn1(cursor, 3)
sjSovevogn1(cursor, 4)

q.db_insert(cursor, "VognOppsett", ['3', '2', '1'])
q.db_insert(cursor, "VognOppsett", ['4', '2', '2'])

q.db_insert(cursor, "Togrute", ['2', 'SJ', "0", 'Trondheim S', 'Bodø'])

q.db_select(cursor, "Stol", ["*"])
q.db_select(cursor, "Kupe", ["*"])
q.db_insert(cursor, "PaRute", ['Trondheim S', '2', '23:05', '23:05'])
q.db_insert(cursor, "PaRute", ['Steinkjer', '2', '00:57', '00:57'])
q.db_insert(cursor, "PaRute", ['Mosjøen', '2', '04:41', '04:41'])
q.db_insert(cursor, "PaRute", ['Mo i Rana', '2', '05:55', '05:55'])
q.db_insert(cursor, "PaRute", ['Fauske', '2', '08:19', '08:19'])
q.db_insert(cursor, "PaRute", ['Bodø', '2', '09:05', '09:05'])

q.db_insert(cursor, "RutePaUkedag", ['2', 'mandag'])
q.db_insert(cursor, "RutePaUkedag", ['2', 'tirsdag'])
q.db_insert(cursor, "RutePaUkedag", ['2', 'onsdag'])
q.db_insert(cursor, "RutePaUkedag", ['2', 'torsdag'])
q.db_insert(cursor, "RutePaUkedag", ['2', 'fredag'])
q.db_insert(cursor, "RutePaUkedag", ['2', 'lørdag'])
q.db_insert(cursor, "RutePaUkedag", ['2', 'søndag'])


q.db_insert(cursor, "RutePaStrekning", ['2', 'Trondheim S', 'Steinkjer'])
q.db_insert(cursor, "RutePaStrekning", ['2', 'Steinkjer', 'Mosjøen'])
q.db_insert(cursor, "RutePaStrekning", ['2', 'Mosjøen', 'Mo i Rana'])
q.db_insert(cursor, "RutePaStrekning", ['2', 'Mo i Rana', 'Fauske'])
q.db_insert(cursor, "RutePaStrekning", ['2', 'Fauske', 'Bodø'])

q.db_insert(cursor, "Togruteforekomst", ['3', '03-04-2023', '2'])
q.db_insert(cursor, "Togruteforekomst", ['4', '04-04-2023', '2'])





#Morgentog fra Mo i Rana til Trondheim 

sjSittevogn1(cursor, 5)
q.db_insert(cursor, "VognOppsett", ['5', '3', '1'])

q.db_insert(cursor, "Togrute", ['3', 'SJ', "1", 'Mo i Rana', 'Trondheim S'])

#stasjoner på ruten 
q.db_insert(cursor, "PaRute", ['Mo i Rana', '3', '08:11', '08:11'])
q.db_insert(cursor, "PaRute", ['Mosjøen', '3', '09:14', '09:14'])
q.db_insert(cursor, "PaRute", ['Steinkjer', '3', '12:31', '12:31'])
q.db_insert(cursor, "PaRute", ['Trondheim S', '3', '14:13', '14:13'])

q.db_insert(cursor, "RutePaUkedag", ['3', 'mandag'])
q.db_insert(cursor, "RutePaUkedag", ['3', 'tirsdag'])
q.db_insert(cursor, "RutePaUkedag", ['3', 'onsdag'])
q.db_insert(cursor, "RutePaUkedag", ['3', 'torsdag'])
q.db_insert(cursor, "RutePaUkedag", ['3', 'fredag'])


q.db_insert(cursor, "RutePaStrekning", ['3', 'Mo i Rana', 'Mosjøen'])
q.db_insert(cursor, "RutePaStrekning", ['3', 'Mosjøen', 'Steinkjer'])
q.db_insert(cursor, "RutePaStrekning", ['3', 'Steinkjer', 'Trondheim S'])


q.db_insert(cursor, "Togruteforekomst", ['5', '03-04-2023', '3'])
q.db_insert(cursor, "Togruteforekomst", ['6', '04-04-2023', '3'])



con.commit()

q.db_select(cursor, "Togrute", ["*"])
q.db_select(cursor, "Vogn", ["*"])
q.db_select(cursor, "Stol", ["*"])



print(cursor.fetchall())


con.close()





