import queries as q


"""Pre-defined commonly used queries"""


def func_get_all_routes(cursor, station_name: str, weekday:str ) :

    q.db_select(cursor, "Togrute", ["RuteID"], [f"StartstasjonNavn = '{station_name}'"])


def create_user(cursor, KundeNr: str, Navn: str, Epostadresse: str, Mobilnummer: str): 

    q.db_insert(cursor, "Kunde", [KundeNr, Navn, Epostadresse, Mobilnummer])

def find_route(cursor, startstasjon, endestasjon, klokkeslett, dag) : 

    sortert_stasjoner = ['Bodø', 'Fauske', 'Mo i Rana', 'Mosjøen', 'Steinskjer', 'Trondheim']
    ukedager = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag']

    start_index = sortert_stasjoner.index(startstasjon)
    slutt_index = sortert_stasjoner.index(endestasjon)

    ukedag_idx = ukedager.index(dag)

    retning = 0

    if start_index < slutt_index: 
        retning = 1
    else : 
        retning = 0

    quer = f"""
            SELECT * FROM PaRute 
            NATURAL JOIN Togrute 
            NATURAL JOIN RutePaUkedag 
            WHERE Avgangstid>='{klokkeslett}' 
            AND (Ukedag=='{ukedager[ukedag_idx]}' OR Ukedag=='{ukedager[ukedag_idx+1]}') 
            AND StasjonNavn=='{endestasjon}'
            AND Hovedretning=={retning} 
            ORDER BY Avgangstid ASC"""
    
    qstr = str(quer)
    
    cursor.execute(qstr)




