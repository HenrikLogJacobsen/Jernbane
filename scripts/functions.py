import queries as q


"""Pre-defined commonly used queries"""


def func_get_all_routes(cursor, station_name: str, weekday:str ) :

    q.db_select(cursor, "Togrute", ["RuteID"], [f"StartstasjonNavn = '{station_name}'"])

