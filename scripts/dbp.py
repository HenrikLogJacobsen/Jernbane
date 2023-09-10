import sqlite3
import queries as q
import user_functions as uf

con = sqlite3.connect("./db/prosjekt.db")

cursor = con.cursor()




## opg c
# uf.get_all_routes(cursor, "Mosjøen", "onsdag")

# con.commit()

# print(cursor.fetchall())

## opg d

## finner alle ruter som går innom en gitt stasjon etter et gitt klokkeslett en gitt dagen og dagen etter 
# uf.find_route(cursor, 'Steinkjer', 'Mosjøen', '00:00', '03-04-2023')



# con.commit()


# for el in cursor.fetchall() : 
#     print(el)

## opg e
#uf.create_user(cursor, '10', 'Henrik', 'henrik@mail.com', '1939394949')

## opg f
 


## opg d
def get_intervals(cursor, startStasjon, stopStasjon, forekomstID):
    stations = uf.find_nordlandsbanen(cursor)
    intervals = []
    startIdx = -1
    stopIdx = -1
    hovedretning = cursor.execute("""
                    SELECT Hovedretning
                    FROM Togrute
                    NATURAL JOIN TogruteForekomst
                    WHERE ForekomstID = ?
                    """, (forekomstID,)).fetchone()
    
    if (hovedretning is 0):
        startIdx = stations.index(startStasjon)
        stopIdx = stations.index(stopStasjon)
    else:
        startIdx = stations.index(stopStasjon)
        stopIdx = stations.index(startStasjon)
    
    while startIdx is not stopIdx:
        intervals.append((stations[stopIdx], stations[stopIdx - 1]))
        stopIdx -= 1
    
    return intervals

def chair_in_interval(cursor, startStation, stopStation, bookedChair):
    intervals = get_intervals(cursor, startStation, stopStation, bookedChair[2])
    chairIntervals = get_intervals(cursor, bookedChair[3], bookedChair[4], bookedChair[2])

    for i in intervals:
        if i in chairIntervals:
            return True
    return False
    #varr = tuple(get_intervals(cursor, "Trondheim S","Mo i Rana", "1"))

def available_chairs(cursor, startStation, stopStation, allChairs, bookedChairs):

    available = allChairs

    for bookedChair in bookedChairs:
        if chair_in_interval(cursor, startStation, stopStation, bookedChair):
            #remove chair from allchairs
            available.remove((bookedChair[0], bookedChair[1], bookedChair[2]))

    return available



cursor.execute("""
                SELECT DISTINCT Togrute.RuteID, TogruteForekomst.Ukedag, TogruteForekomst.ForekomstID, Seng.SengNr, Seng.KupeNr, Vognoppsett.VognNr, Vogn.VognID
                    FROM ((Togrute 
                    JOIN TogruteForekomst ON TogruteForekomst.TogruteID == Togrute.RuteID
                    NATURAL JOIN Vognoppsett
                    NATURAL JOIN Vogn 
                    JOIN Seng ON Vogn.VognID == Seng.VognID)
                    LEFT OUTER JOIN 
                     Sengebillett ON Seng.KupeNr == SengeBillett.KupeNr)
        
                    WHERE SengeBillett.SengNr IS NULL 
                        AND TogruteForekomst.Ukedag == '03-04-2023'
                    
                    ORDER BY TogruteForekomst.ForekomstID ASC
                """)




# print(cursor.description)
# for el in cursor.fetchall(): 
#     print(el)


# uf.find_route(cursor, 'Trondheim S', 'Bodø', '00:00', '03-04-2023')
# for el in (cursor.fetchall()): 
#     print(el)

# cursor.execute(""" 
#                 INSERT INTO Kundeordre VALUES ('2', '2', '12', '123', '10', 'Trondheim S', 'Bodø')
#                 """)

# cursor.execute(""" 
#                 INSERT INTO SengeBillett VALUES ('1', '2', '1', '1', '1')
#                 """)


# uf.buy_ticket_seng(cursor, 10, 2, 'Mosjøen', 'Bodø', '00:00', '04-04-2023', [3,4], 2)


# uf.available_tickets(cursor, "stol", "03-04-2023")
# for el in cursor.fetchall(): 
#     print(el)

# cursor.execute("DELETE FROM SengeBillett")
# cursor.execute("DELETE FROM Kundeordre")
# cursor.execute("DELETE FROM Sittebillett")

print("-------------------------------------------------------------------------------------------------------------------------------------")


# startstasjoner = ('')
# cursor.execute(f"""
#                 SELECT Stol.StolNr, Vognoppsett.VognNr, Togruteforekomst.forekomstid
#                 FROM 
#                 Stol
#                 NATURAL JOIN Vogn
#                 NATURAL JOIN Vognoppsett 
#                 JOIN Togruteforekomst ON Togruteforekomst.TogruteID == Vognoppsett.RuteID

#                 WHERE Togruteforekomst.Ukedag == '03-04-2023' 
#                     AND Togruteforekomst.ForekomstID == '1'
                    
                    
#                 ORDER BY Vognoppsett.Vognnr
#                 """)


# ledige_start =  cursor.fetchall()

# alleStoler = []

# for el in ledige_start:

#     alleStoler.append(el)



# cursor.execute(f""" 
#                 SELECT sittebillett.stolnr, sittebillett.vognnr, kundeordre.forekomstID, kundeordre.startstasjon, kundeordre.endestasjon
#                 FROM
#                 Sittebillett 
#                 NATURAL JOIN Kundeordre
#                 NATURAL JOIN Togruteforekomst
#                 WHERE togruteforekomst.Ukedag == '03-04-2023'
#                 AND Togruteforekomst.forekomstID = '1'
#                 """)




# print("------------------------------------------------------------------------------------------------")

# cursor.execute(f"""
#                     SELECT Sengebillett.sengnr, sengebillett.kupenr, sengebillett.vognrnr, kundeordre.forekomstID, togruteforekomst.ukedag FROM 
#                     SengeBillett 
#                     NATURAL JOIN Kundeordre 
#                     NATURAL JOIN Togruteforekomst
#                     WHERE togruteforekomst.ukedag == '03-04-2023'
#                     """)


# cursor.execute(f"""  
#                 SELECT seng.sengnr, seng.kupenr, vognoppsett.vognnr, togruteforekomst.forekomstid, togruteforekomst.ukedag FROM 
#                 seng
#                 NATURAL JOIN Vogn 
#                 NATURAL JOIN Vognoppsett
#                 JOIN Togruteforekomst ON Togruteforekomst.togruteID == Vognoppsett.ruteid
        
#                 """)




# cursor.execute(f""" 
#                 SELECT seng.sengnr, seng.kupenr, vognoppsett.vognnr, togruteforekomst.forekomstid, togruteforekomst.ukedag FROM 
#                 seng
#                 NATURAL JOIN Vogn 
#                 NATURAL JOIN Vognoppsett
#                 JOIN Togruteforekomst ON (Togruteforekomst.togruteID == Vognoppsett.ruteid AND Togruteforekomst.ukedag=='04-04-2023')

#                 EXCEPT 

#                 SELECT Sengebillett.sengnr, sengebillett.kupenr, sengebillett.vognrnr, kundeordre.forekomstID, togruteforekomst.ukedag FROM 
#                 SengeBillett 
#                 NATURAL JOIN Kundeordre 
#                 NATURAL JOIN Togruteforekomst
#                 WHERE togruteforekomst.ukedag == '04-04-2023'

#                 """)


# uf.buy_ticket_stol(cursor, 10, 1, "Steinkjer", "Fauske", "00:00", "03-04-2023", [1], 1)
#uf.buy_ticket_seng(cursor, 10, 2, 'Steinkjer', 'Mosjøen', '00:00', '04-04-2023', [5, 6], 2)

# ava = uf.available_tickets(cursor, 'seng', '03-04-2023',  '2')
# print("SengeNr - KupeNr - VognNr")
# for el in ava: 
#     print("  ", el[0], "   |   ", el[1],"  |   ",el[2])


# ava = uf.available_tickets(cursor, 'stol', '03-04-2023',  '3')
# print("StolNr - VognNr - Togruteforekomst")
# for el in ava: 
#     print("  ", el[0], "   |   ", el[1],"  |       ",el[2])

rute = uf.find_route(cursor, "Steinkjer", "Bodø", "00:00", "03-04-2023")

print(rute)
#print(uf.getOrderInfo(cursor, 10))

# cursor.execute("SELECT kunde.kundenr FROM kunde WHERE kundenr=='23'")

# kunder = cursor.fetchall()

# print(len(kunder) == 1)
     

con.commit()



con.close()


lst = [(1, 1, 2, 4, '04-04-2023'), (2, 1, 2, 4, '04-04-2023'), (5, 3, 2, 4, '04-04-2023'), (6, 3, 2, 4, '04-04-2023'), (7, 4, 2, 4, '04-04-2023'), (8, 4, 2, 4, '04-04-2023')]
beds = {(5, 3, 2, 4, '04-04-2023'), (6, 3, 2, 4, '04-04-2023')}

print(beds.issubset(lst))