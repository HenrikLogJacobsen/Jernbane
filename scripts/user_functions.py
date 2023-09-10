import queries as q
from datetime import date
from datetime import datetime


import re

pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

"""Pre-defined commonly used queries"""


def get_all_routes(cursor, stasjonsnavn: str, ukedag:str ) :

#     """ 
#     brukerhistorie c , finner alle ruter som går innom en stasjon på en gitt ukedag
#     INPUT: 
#             stasjonsnavn: den statsjonen vi vil finne alle rutene som går innom
#             ukedag: dagen vi vil ha rutene  
#     """

        quer = """
        SELECT Togrute.*
        FROM Togrute
        NATURAL JOIN RutePaUkedag
        NATURAL JOIN PaRute
        WHERE StasjonNavn = ?
        AND Ukedag = ?
        """
    
        qstr = str(quer)

        cursor.execute(qstr, (stasjonsnavn, ukedag))
        



def create_user(cursor, Navn: str, Epostadresse: str, Mobilnummer: str): 

    """
    brukerhistorie e, legger til en kunde i databasen
    INPUT: 
            KundeNr: kundenummeret til kunden (burde ver noe automatikk i den)
            Navn: navn til kunden 
            Epostadresse: epostadresse til kunden
            Mobilnummer: mobilnummer til kunden
    """
    if (not re.match(pat, Epostadresse)):
        raise Exception("Ugyldig email")
    
    if (len(Mobilnummer) != 8):
        raise Exception("Feil lengde på mobilnummer")
    
    try:
        int(Mobilnummer)
    except Exception as e:
        raise Exception("Mobilnummer kan bare bestå av tall")

    #Ny bruker vil ha ett høyere kundenummer enn det høyeste som finnes fra før
    KundeNr = str(cursor.execute("SELECT MAX(KundeNr) FROM Kunde").fetchone()[0] + 1)

    q.db_insert(cursor, "Kunde", [KundeNr, Navn, Epostadresse, Mobilnummer])


def find_nordlandsbanen(cursor):
    cursor.execute('''
        SELECT D1.EndestasjonNavn
        FROM Delstrekning AS D1
        INNER JOIN Delstrekning AS D2 ON D1.StartstasjonNavn = D2.EndestasjonNavn
        WHERE D1.BanestrekningNavn = 'Nordlandsbanen'
        UNION
        SELECT D3.StartstasjonNavn
        from Delstrekning AS D3
        WHERE D3.BanestrekningNavn = 'Nordlandsbanen'
    ''')
    nordlandsbanen = []
    for row in cursor:
         nordlandsbanen.append(row[0])

    return nordlandsbanen


def find_route(cursor, startstasjon, endestasjon, klokkeslett, dag) : 

    """ 
    brukerhistorie d, søker etter en rute som går mellom en gitt start og sluttstasjon på en gitt dato etter et gitt klokkeslett
    INPUT: 
            startstasjon: stasjonen kunden reiser fra
            endestasjon: stasjonen kunden reiser til
            klokkeslett: klokkeslett som ruten tidligst skal gå
            dag: ukedagen ruten skal gå

    OUTPUT: 
            gir ut alle ruter som oppfyller kravene til input, for ukedagen søkt på og dagen etter
    """

    sortert_stasjoner = find_nordlandsbanen(cursor)

    start_index = sortert_stasjoner.index(startstasjon)
    slutt_index = sortert_stasjoner.index(endestasjon)

    retning = 0

    if start_index < slutt_index: 
        retning = 1
    else : 
        retning = 0

    quer = """
        SELECT DISTINCT TogRute.*, TogruteForekomst.Ukedag, Avgangstid
        FROM PaRute
        NATURAL JOIN Togrute 
        NATURAL JOIN TogruteForekomst
        WHERE 
        ((Avgangstid >= ? AND TogruteForekomst.Ukedag == ?)
        OR TogruteForekomst.Ukedag >= ?)
        AND StasjonNavn = ?
        AND Hovedretning = ?
        ORDER BY TogruteForekomst.Ukedag ASC, Avgangstid ASC
        """
    
    qstr = str(quer)
    
    cursor.execute(qstr,(klokkeslett, dag, dag, startstasjon, retning))

    routes = cursor.fetchall()
    return routes
    
def available_tickets (cursor, type, dato, togruteID) :

    cursor.execute(f"SELECT togruteforekomst.forekomstid FROM togruteforekomst where togruteforekomst.ukedag == '{dato}' AND togruteforekomst.togruteid == '{togruteID}'")

    forekomst = cursor.fetchall()[0]
    forekomst = forekomst[0]
    print(forekomst)


    cursor.execute(f"SELECT * FROM Vognoppsett NATURAL JOIN Vogn WHERE RuteID == '2'")
    vogntyper = []
    for el in cursor.fetchall(): 
        vogntyper.append(el[3])

    
    if type == 'seng': 

        cursor.execute(f"""
                SELECT seng.sengnr, seng.kupenr, vognoppsett.vognnr, togruteforekomst.forekomstid, togruteforekomst.ukedag FROM 
                seng
                NATURAL JOIN Vogn 
                NATURAL JOIN Vognoppsett
                JOIN Togruteforekomst ON (Togruteforekomst.togruteID == Vognoppsett.ruteid AND Togruteforekomst.ukedag=='{dato}' AND Togruteforekomst.forekomstid == '{forekomst}')

                EXCEPT 

                SELECT DISTINCT seng.sengnr, sengebillett.kupenr, sengebillett.vognrnr, kundeordre.forekomstID, togruteforekomst.ukedag FROM 
                SengeBillett 
                NATURAL JOIN Kundeordre 
                NATURAL JOIN Togruteforekomst
                JOIN Seng ON Seng.kupenr == Sengebillett.kupenr
                WHERE togruteforekomst.ukedag == '{dato}'
                """)
        ava = cursor.fetchall()
        return ava
        
    elif type == 'stol': 

        cursor.execute(f"""
                SELECT Stol.StolNr, Vognoppsett.VognNr, Togruteforekomst.forekomstid
                FROM 
                Stol
                NATURAL JOIN Vogn
                NATURAL JOIN Vognoppsett 
                JOIN Togruteforekomst ON Togruteforekomst.TogruteID == Vognoppsett.RuteID

                WHERE Togruteforekomst.Ukedag == '{dato}' 
                    AND Togruteforekomst.ForekomstID == '{forekomst}'
                    
                    
                ORDER BY Vognoppsett.Vognnr
                """)


        alleStoler =  cursor.fetchall()

        cursor.execute(f""" 
                SELECT sittebillett.stolnr, sittebillett.vognnr, kundeordre.forekomstID, kundeordre.startstasjon, kundeordre.endestasjon
                FROM
                Sittebillett 
                NATURAL JOIN Kundeordre
                NATURAL JOIN Togruteforekomst
                WHERE togruteforekomst.Ukedag == '{dato}'
                AND Togruteforekomst.forekomstID = '{forekomst}'
                """)

        opptatteStoler =  cursor.fetchall()

        ava = available_chairs(cursor, "Steinkjer", "Fauske", alleStoler, opptatteStoler)
        return ava

        

def buy_ticket_seng(cursor, kundeNr, RuteID, startstasjon, endestasjon, klokkeslett, dato, sengNr, vognNr):

    cursor.execute(f"SELECT kunde.kundenr FROM kunde WHERE kundenr=='{kundeNr}'")

    kunder = cursor.fetchall()

    if len(kunder) != 1: 
        print("må være kunde for å kjøpe billett")
        
    cursor.execute("SELECT * FROM SengeBillett ORDER BY BilettNr DESC")

    Billett = cursor.fetchall()
    if Billett: 
        BillettNr = Billett[0][0]+1
    else: 
        BillettNr = 1

    cursor.execute("SELECT * FROM KundeOrdre ORDER BY OrdreNr DESC")

    Ordre = cursor.fetchall()
    if Ordre: 
        OrdreNr = Ordre[0][0]+1
    else: 
        OrdreNr=1

    cursor.execute(f"SELECT * FROM TogruteForekomst WHERE Ukedag=='{dato}' AND TogruteID == '{RuteID}'")

    forekomst = cursor.fetchall()[0][0]

    cursor.execute(f"SELECT kupeNr FROM Seng WHERE SengNr == {sengNr[0]}")

    kupeNr = cursor.fetchall()[0][0]

    if len(sengNr) > 1 :    
        if not (sengNr[0]%2==1 and sengNr[0]+1==sengNr[1]): 
            print("senger må ver i samme kupee eeeee eee e e e e e ee ee ")
            return 


    print(dato, RuteID)
    lst = available_tickets(cursor, "seng", dato, RuteID)
   
    beds = set()
    
    for nr in sengNr: 
        beds.add((nr, kupeNr, vognNr, forekomst, dato))

    print(lst)
    print(beds)

        
    if beds.issubset(lst) : 
        # good 
        print("good")


        cursor.execute(f""" 
                    INSERT INTO Kundeordre VALUES ('{OrdreNr}', '{forekomst}', 'NULL', 'NULL', '{kundeNr}', '{startstasjon}', '{endestasjon}')
                    """)

        for bed in beds: 

            cursor.execute(f""" 
                    INSERT INTO SengeBillett VALUES ('{BillettNr}', '{OrdreNr}', '{bed[0]}', '{vognNr}', '{bed[1]}')
                    """)
            BillettNr += 1 
        
    else: 
        #good`nt
        print("Seng opptatt")



        
def buy_ticket_stol(cursor, kundeNr, RuteID, startstasjon, endestasjon, klokkeslett, dato, stolNr, vognNr): 

    cursor.execute("SELECT * FROM SitteBillett ORDER BY BillettNr DESC")

    Billett = cursor.fetchall()
    if Billett: 
        BillettNr = Billett[0][0]+1
    else: 
        BillettNr = 1

    cursor.execute("SELECT * FROM KundeOrdre ORDER BY OrdreNr DESC")

    Ordre = cursor.fetchall()
    if Ordre: 
        OrdreNr = Ordre[0][0]+1
    else: 
        OrdreNr=1

    cursor.execute(f"SELECT * FROM TogruteForekomst WHERE Ukedag=='{dato}' AND TogruteID == '{RuteID}'")

    forekomst = cursor.fetchall()[0][0]

    cursor.execute(f"SELECT VognID FROM Vognoppsett WHERE VognNr={vognNr} AND RuteID={RuteID}")
    vognID = cursor.fetchall()[0][0]


    lst = available_tickets(cursor, 'stol', dato, RuteID)
    
    chairs = set()

    for chair in stolNr: 

        chairs.add((chair, vognNr, forekomst))
    
    print(chairs)

    if ( chairs.issubset(lst) ) : 
        print("good") 
        cursor.execute(f""" 
                    INSERT INTO Kundeordre VALUES ('{OrdreNr}', '{forekomst}', 'NULL', 'NULL', '{kundeNr}', '{startstasjon}', '{endestasjon}')
                    """)

        for chair in chairs: 

            cursor.execute(f""" 
                    INSERT INTO SitteBillett VALUES ('{BillettNr}', '{OrdreNr}', '{chair[0]}', '{vognNr}')
                    """)
            BillettNr += 1 

    else: 
        print("stol tatt ")


    
    






## KOMPLIMENTÆRE FUNKSJONER 

def get_intervals(cursor, startStasjon, stopStasjon, forekomstID):
    stations = find_nordlandsbanen(cursor)
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
    print(available)
    
    for bookedChair in bookedChairs:
        if chair_in_interval(cursor, startStation, stopStation, bookedChair):
            #remove chair from allchairs
            print(bookedChair)
            available.remove((bookedChair[0], bookedChair[1], bookedChair[2]))

    return available


def getOrderInfo(cursor, KundeNr):
    today_str = date.today().strftime("%d-%m-%Y")
    today = datetime.strptime(today_str, '%d-%m-%Y').date()
    seats = []
    beds = []
    cursor.execute(f"""
        SELECT Kundeordre.ordreNr, Kunde.Navn, Kundeordre.startstasjon, parute.avgangstid, Kundeordre.endestasjon, TogruteForekomst.ukedag
        FROM Kunde
        NATURAL JOIN Kundeordre
        NATURAL JOIN Togruteforekomst
        JOIN parute ON parute.ruteID == TogruteForekomst.togruteID AND Kundeordre.startstasjon == parute.stasjonnavn
        WHERE Kunde.KundeNr == '{KundeNr}'
    """)
    kundeinfo = cursor.fetchall()
    print("kundeinfo lengde: ", len(kundeinfo)) 
    updatedinfo = []
    for el in kundeinfo:
        date_str = el[-1]
        temp_date = datetime.strptime(date_str, '%d-%m-%Y').date()
        if temp_date > today:
            updatedinfo.append(el)
    cursor.execute(f"""
                    SELECT sengebillett.ordreNr FROM Sengebillett
        """)
    bedlist = [x[0] for x in cursor.fetchall()]

    cursor.execute(f"""
                    SELECT sittebillett.ordreNr FROM sittebillett
    """)
    seatlist = [x[0] for x in cursor.fetchall()]
    for el in updatedinfo:
        print("el: ", el[0], "list: ", seatlist)
        if el[0] in seatlist:
            seats.append(getseatnums(cursor, el[0]))
        else:
            beds.append(getbednums(cursor, el[0]))
    print("seats: ", seats)
    print("beds: ", beds)
    return updatedinfo

def getseatnums(cursor, orderNr):
    temp = []
    cursor.execute(f"""
                SELECT sittebillett.stolnr, sittebillett.vognNr FROM sittebillett
                WHERE sittebillett.ordreNr == '{orderNr}'
    """)
    temp.append(el for el in cursor.fetchall())
    #temp = cursor.fetchall()
    return temp

def getbednums(cursor, orderNr):
    temp = []
    cursor.execute(f"""
                SELECT sengebillett.sengNr, sengebillett.vognrNr, seng.kupeNr
                FROM sengebillett
                NATURAL JOIN seng
                WHERE sengebillett.ordreNr == '{orderNr}'
    """)
    temp.append(el for el in cursor.fetchall())
    #temp = cursor.fetchall()
    print("temp: ", temp)
    return temp
    




# [(10, 1, 1, 'NULL', 'NULL', 10, 'Steinkjer', 'Fauske', '03-04-2023'),
#  (10, 2, 4, 'NULL', 'NULL', 10, 'Mosjøen', 'Bodø', '04-04-2023')]



    #  cursor.execute(f""" 
    #             SELECT sittebillett.stolnr, sittebillett.vognnr, kundeordre.forekomstID, kundeordre.startstasjon, kundeordre.endestasjon
    #             FROM
    #             Sittebillett 
    #             NATURAL JOIN Kundeordre
    #             NATURAL JOIN Togruteforekomst
    #             WHERE togruteforekomst.Ukedag == '03-04-2023'
    #             AND Togruteforekomst.forekomstID = '1'
    #             """)
                    #JOIN sengebillett ON sengebillett.OrdreNR == Kundeordre.OrdreNr
                    #JOIN seng ON sengebillett.sengNr == seng.sengNR