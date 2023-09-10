import sqlite3
import queries as q


def sjSittevogn1 (cursor, vognId):
    totalChairs = 12
    # MERK: Type-attributtet er 1 for sittevogn, 0 for sovevogn
    q.db_insert(cursor, "Vogn", [vognId, 1, "SJ-sittevogn-1", None, 4, "SJ"])

    for chairNumber in range(1, totalChairs + 1):
        q.db_insert(cursor, "Stol", [vognId, chairNumber])
