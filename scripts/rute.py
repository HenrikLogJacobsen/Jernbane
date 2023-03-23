import queries as q

weekdays = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
weekend = ["Lørdag", "Søndag"]

def routeWholeWeek (cursor, routeId):
    for day in weekdays + weekend:
        q.db_insert(cursor, "RutePaUkedag", [str(routeId), day])

def routeMonToFri (cursor, routeId):
    for day in weekdays:
        q.db_insert(cursor, "RutePaUkedag", [str(routeId), day])
        


