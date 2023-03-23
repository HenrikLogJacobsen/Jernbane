import queries as q

def sjSittevogn1 (cursor, vognId):
    totalChairs = 12
    # MERK: Type-attributtet er 1 for sittevogn, 0 for sovevogn
    q.db_insert(cursor, "Vogn", [str(vognId), '1', "SJ-sittevogn-1", None, '4', "SJ"])

    for chairNumber in range(1, totalChairs + 1):
        q.db_insert(cursor, "Stol", [str(vognId), str(chairNumber)])

def sjSovevogn1 (cursor, vognId):
    totalRooms = 4
    bedsPerRoom = 2
    # MERK: Type-attributtet er 1 for sittevogn, 0 for sovevogn
    q.db_insert(cursor, "Vogn", [str(vognId), '0', "SJ-sovevogn-1", str(bedsPerRoom), None, "SJ"])

    bedId = 1
    for roomNr in range(1, totalRooms + 1):
        q.db_insert(cursor, "Kupe", [str(vognId), str(roomNr)])
        for _ in range(bedsPerRoom):
            q.db_insert(cursor, "Seng", [str(vognId), str(bedId), str(roomNr)])
            bedId += 1


