import queries as q
from datetime import date
from datetime import datetime


import re

pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# Pre-defined commonly used queries

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

    routes = cursor.fetchall()
    if len(routes) == 0: 
    
        raise Exception("ingen ruter som matcher søket.")
    return routes

def create_user(cursor, Navn: str, Epostadresse: str, Mobilnummer: str): 

    """
    brukerhistorie e, legger til en kunde i databasen
    INPUT: 
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
    KundeNr = (cursor.execute("SELECT MAX(KundeNr) FROM Kunde").fetchone()[0])
    if not KundeNr : 
        KundeNr = str(1)
    else: 
        KundeNr = str(KundeNr+1)

    cursor.execute("INSERT INTO Kunde (KundeNr, Navn, Epostadresse, Mobilnummer) VALUES(?, ?, ?, ?)", (KundeNr, Navn, Epostadresse, Mobilnummer))

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
            dag: datoen ruten skal gå

    OUTPUT: 
           liste med alle ruter som oppfyller kravene til input, for datoen søkt på og dagen etter
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
    if len(routes) == 0: 
        raise Exception("ingen ruter som matcher søket")
    
    return routes
    
def available_tickets (cursor, type, dato, togruteID) :

    """
    Finner alle ledige sitte/ sove plasser på en spesifik togrute forekomst.
    INPUT: 
            type: "seng" eller "stol", spesifiserer typen billett man vil se etter.
            dato: datoen man vil se på billett, format "dd-mm-yyyy"
            togruteID: 1, 2 eller 3, spesifiserer den ruten man skal ta
    OUTPUT: 
            en liste med alle ledige plasser på toget, sengeplasser eller sitteplasser.
     
    """

    cursor.execute("SELECT togruteforekomst.forekomstid FROM togruteforekomst where togruteforekomst.ukedag == ? AND togruteforekomst.togruteid == ?", (dato, togruteID))

    forekomst = cursor.fetchall()[0]
    forekomst = forekomst[0]
  
    if type == 'seng': 

        cursor.execute("""
                SELECT seng.sengnr, seng.kupenr, vognoppsett.vognnr, togruteforekomst.forekomstid, togruteforekomst.ukedag FROM 
                seng
                NATURAL JOIN Vogn 
                NATURAL JOIN Vognoppsett
                JOIN Togruteforekomst ON (Togruteforekomst.togruteID == Vognoppsett.ruteid AND Togruteforekomst.ukedag==? AND Togruteforekomst.forekomstid == ?)

                EXCEPT 

                SELECT DISTINCT seng.sengnr, sengebillett.kupenr, sengebillett.vognrnr, kundeordre.forekomstID, togruteforekomst.ukedag FROM 
                SengeBillett 
                NATURAL JOIN Kundeordre 
                NATURAL JOIN Togruteforekomst
                JOIN Seng ON Seng.kupenr == Sengebillett.kupenr
                WHERE togruteforekomst.ukedag == ?
                """, (dato, forekomst, dato))
        ava = cursor.fetchall()

        if len(ava) == 0: 
            raise Exception("Ingen ledige reise ved gitt søk")
        return ava
        
    elif type == 'stol': 

        cursor.execute(f"""
                SELECT Stol.StolNr, Vognoppsett.VognNr, Togruteforekomst.forekomstid
                FROM 
                Stol
                NATURAL JOIN Vogn
                NATURAL JOIN Vognoppsett 
                JOIN Togruteforekomst ON Togruteforekomst.TogruteID == Vognoppsett.RuteID

                WHERE Togruteforekomst.Ukedag == ? 
                    AND Togruteforekomst.ForekomstID == ?
                    
                    
                ORDER BY Vognoppsett.Vognnr
                """, (dato, forekomst))


        alleStoler =  cursor.fetchall()

        cursor.execute(f""" 
                SELECT sittebillett.stolnr, sittebillett.vognnr, kundeordre.forekomstID, kundeordre.startstasjon, kundeordre.endestasjon
                FROM
                Sittebillett 
                NATURAL JOIN Kundeordre
                NATURAL JOIN Togruteforekomst
                WHERE togruteforekomst.Ukedag == ?
                AND Togruteforekomst.forekomstID = ?
                """, (dato, forekomst))

        opptatteStoler =  cursor.fetchall()

        ava = available_chairs(cursor, "Steinkjer", "Fauske", alleStoler, opptatteStoler)
        if len(ava) == 0: 
            raise Exception("Ingen plasser som matcher søket.")
        return ava
    
def buy_ticket_seng(cursor, kundeNr, RuteID, startstasjon, endestasjon, dato, sengNr, vognNr):

    """" 
    oppretter en billett og legger den inn i databasen gitt at input oppfyller krav. Sjekker om biletten er mot en seng som er ledig. 
    INPUT: 
            kundeNr: kunden som skal kjøpe billett, må være bruker for å kjøpe
            RuteID: ruten man vil kjøpe billett på 
            start- og endestasjon: hvor man vil reise fra / til 
            dato: datoen man skal kjøpe billett for
            sengNr: sengen på toget man vil kjøpe 
            vognNr: hvilken av vognene til sengen. Denne med sengNr utgjør en spesifik seng på toget. 
    
    """

    cursor.execute("SELECT kunde.kundenr FROM kunde WHERE kundenr== ? ", (kundeNr, ))

    kunder = cursor.fetchall()

    if len(kunder) != 1: 
        raise Exception("Du må være kunde for å kjøpe billett")
        
        
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

    cursor.execute("SELECT * FROM TogruteForekomst WHERE Ukedag== ? AND TogruteID == ?", (dato, RuteID))

    forekomst = cursor.fetchall()[0][0]

    cursor.execute("SELECT kupeNr FROM Seng WHERE SengNr == ?", (sengNr[0], ))

    kupeNr = cursor.fetchall()[0][0]

    if len(sengNr) > 1 :    
        if not (sengNr[0]%2==1 and sengNr[0]+1==sengNr[1]): 
            raise Exception("senger må ver i samme kupee eeeee eee e e e e e ee ee ") 


    lst = available_tickets(cursor, "seng", dato, RuteID)
   
    beds = set()
    
    for nr in sengNr: 
        beds.add((nr, kupeNr, vognNr, forekomst, dato))

    if beds.issubset(lst) : 
        cursor.execute(""" 
                    INSERT INTO Kundeordre VALUES (?, ?, 'NULL', 'NULL', ?, ?, ?)
                    """, (OrdreNr, forekomst, kundeNr, startstasjon, endestasjon))

        for bed in beds: 

            cursor.execute(""" 
                    INSERT INTO SengeBillett VALUES (?, ?, ?, ?, ?)
                    """, (BillettNr, OrdreNr, bed[0], vognNr, bed[1]))
            BillettNr += 1 

            print(f"KJØP: BillettNR: {BillettNr} | OrdreNr: {OrdreNr} | SengNr: {bed[0]} | VognNr: {vognNr}")
        
    else: 
        raise Exception("Seng opptatt")
        
def buy_ticket_stol(cursor, kundeNr, RuteID, startstasjon, endestasjon, dato, stolNr, vognNr): 

    """" 
    oppretter en billett og legger den inn i databasen gitt at input oppfyller krav. Sjekker om biletten er mot en stol som er ledig. 
    INPUT: 
            kundeNr: kunden som skal kjøpe billett, må være bruker for å kjøpe
            RuteID: ruten man vil kjøpe billett på 
            start- og endestasjon: hvor man vil reise fra / til 
            dato: datoen man skal kjøpe billett for
            stolNr: sengen på toget man vil kjøpe 
            vognNr: hvilken av vognene til sengen. Denne med stolNr utgjør en spesifik stol på toget. 
    
    """
    cursor.execute("SELECT kunde.kundenr FROM kunde WHERE kundenr== ? ", (kundeNr, ))

    kunder = cursor.fetchall()

    if len(kunder) != 1: 
        raise Exception("Du må være kunde for å kjøpe billett")
    
    cursor.execute("SELECT * FROM SitteBillett ORDER BY BillettNr DESC")

    Billett = cursor.fetchall()
    if Billett: 
        BillettNr = Billett[0][0]+1
    else: 
        BillettNr = 1

    cursor.execute("SELECT * FROM KundeOrdre ORDER BY OrdreNr DESC")

    Ordre = cursor.fetchall()
    if Ordre: 
        OrdreNr = str(Ordre[0][0]+1)
    else: 
        OrdreNr=str(1)

    cursor.execute("SELECT * FROM TogruteForekomst WHERE Ukedag== ? AND TogruteID == ?", (dato,RuteID))
    forekomst = cursor.fetchall()[0][0]

    quer = "SELECT VognID FROM Vognoppsett WHERE VognNr=? AND RuteID=?"
    cursor.execute("SELECT VognID FROM Vognoppsett WHERE VognNr=? AND RuteID=?", (vognNr,RuteID))
    vognID = cursor.fetchall()[0][0]


    lst = available_tickets(cursor, 'stol', dato, RuteID)
    
    chairs = set()

    for chair in stolNr: 

        chairs.add((chair, vognNr, forekomst))
    
    if ( chairs.issubset(lst) ) : 
        quer = """ 
                    INSERT INTO Kundeordre VALUES (?,?, 'NULL', 'NULL', ?, ?, ?)
                    """
        cursor.execute(quer, (OrdreNr,forekomst,kundeNr,startstasjon,endestasjon))
        for chair in chairs: 

            c = chair[0]

            quer = """ 
                    INSERT INTO SitteBillett (BillettNr, OrdreNr, StolNr, VognNr) VALUES (?,?,?,?)
                    """
            cursor.execute(quer, (BillettNr, OrdreNr, c, vognNr))
            BillettNr += 1 
            print(f"KJØP: BillettNR: {BillettNr} | OrdreNr: {OrdreNr} | StolNr: {chair[0]} | VognNr: {vognNr}")

    else: 
        raise Exception("stol tatt")
    
def getOrderInfo(cursor, KundeNr):
    """
    Tar inn KundeNr og gir ut informasjon om ordre knyttet til det kundenummeret. 
    Biletter på togruter som har vært blir ikke tatt med ettersom brukerhistorien pressiserte dette.
    INPUT: 
            KundeNr: Kundenummeret til den aktuelle kunden. 
    """

    today_str = date.today().strftime("%d-%m-%Y")
    today = datetime.strptime(today_str, '%d-%m-%Y').date()
    seats = []
    beds = []
    quer = """
        SELECT Kundeordre.ordreNr, Kunde.Navn, Kundeordre.startstasjon, parute.avgangstid, Kundeordre.endestasjon, TogruteForekomst.ukedag
        FROM Kunde
        NATURAL JOIN Kundeordre
        NATURAL JOIN Togruteforekomst
        JOIN parute ON parute.ruteID == TogruteForekomst.togruteID AND Kundeordre.startstasjon == parute.stasjonnavn
        WHERE Kunde.KundeNr == ?
    """
    cursor.execute(quer, (KundeNr,))
    kundeinfo = cursor.fetchall()

    if len(kundeinfo) == 0:
        raise Exception("Finner ingen ordre på denne kunden")

    updatedinfo = []
    #Fjerner tidligere billetter
    for el in kundeinfo:
        date_str = el[-1]
        temp_date = datetime.strptime(date_str, '%d-%m-%Y').date()
        if temp_date > today:
            updatedinfo.append(el)

    cursor.execute(f"""
                    SELECT sittebillett.ordreNr FROM sittebillett
    """)
    seatlist = [x[0] for x in cursor.fetchall()]

    resinfo = []

    billettet = []

    # Formatterer informasjonen til å kunne vises til bruker
    for el in updatedinfo:
        if el[0] in seatlist:
            l = getseatnums(cursor, el[0])
            for elmnt in l:
                
                stolnr = elmnt[0]
                vognnr = elmnt[1]

                seats.append(elmnt)

                billettet.append([el[1], "stol", stolnr, vognnr, " ", el[2], el[3], el[4], el[5]])
        else:
            l = getbednums(cursor, el[0])
            for elmnt in l:
        

                sengnr = elmnt[0]
                vognnr = elmnt[1]
                kupenr = elmnt[2]
               
                billettet.append([el[1], "seng", sengnr, vognnr, kupenr, el[2], el[3], el[4], el[5]])

                resinfo.append(el)
                beds.append(elmnt)

    return billettet

## KOMPLIMENTÆRE FUNKSJONER 

def get_intervals(cursor, startStasjon, stopStasjon, forekomstID):
    """
    Hjelpefunksjon til available_tickets
    OUTPUT: alle delstrekninger mellom to stasjoner
    """
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
    """ 
    Hjelpefunksjon til available_tickets
    """
    intervals = get_intervals(cursor, startStation, stopStation, bookedChair[2])
    chairIntervals = get_intervals(cursor, bookedChair[3], bookedChair[4], bookedChair[2])

    for i in intervals:
        if i in chairIntervals:
            return True
    return False
    #varr = tuple(get_intervals(cursor, "Trondheim S","Mo i Rana", "1"))

def available_chairs(cursor, startStation, stopStation, allChairs, bookedChairs):

    """
    Hjelpefunksjon til available_tickets
    """

    available = allChairs
    
    for bookedChair in bookedChairs:
        if chair_in_interval(cursor, startStation, stopStation, bookedChair):
            #remove chair from allchairs
            available.remove((bookedChair[0], bookedChair[1], bookedChair[2]))

    return available

def getseatnums(cursor, orderNr):
    """
    Hjelpefunksjon til getOrderInfo som gir en liste over seter knyttet til denne kunden
    INPUT:
            ordreNR: Ordrenummer til ordren 
    OUTPUT:
            En liste med stolnummer, vognnummer knyttet til sete(r) på denne ordren

    """
    
    quer = """
                SELECT sittebillett.stolnr, sittebillett.vognNr FROM sittebillett
                WHERE sittebillett.ordreNr == ?
    """
    cursor.execute(quer, (orderNr, ))
    temp = [list(x) for x in cursor.fetchall()]
    return temp

def getbednums(cursor, orderNr):
    """
    Hjelpefunksjon til getOrderInfo som gir en liste over senger knyttet til denne kunden
    INPUT:
            ordreNR: Ordrenummer til ordren 
    OUTPUT:
            En liste med sengenummer, vognnummer og kupenummer knyttet til seng(ene) på denne ordren
    """

    quer = """
                SELECT sengebillett.sengNr, sengebillett.vognrNr, seng.kupeNr
                FROM sengebillett
                NATURAL JOIN seng
                WHERE sengebillett.ordreNr == ?
    """
    cursor.execute(quer, (orderNr, ))
    temp = [list(x) for x in cursor.fetchall()]
    return temp


