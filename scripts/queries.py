import sqlite3

def db_insert(cursor , table_name: str, values: list[str]) :

    """
    Insert into Database
    INPUTS: current cursor, 
            table_name: name of the table you want to add into, 
            values: the values that are being added, make sure to add the correct amount of values
                also in the right order. 
    """

    s = f'{values[0]}' if values[0] else ""

    for i in range(1, len(values)): 
        s += ", " + "'" +values[i]+"'"  if values[i] else ", null"

    try:
        quer = f"INSERT INTO '{table_name}' VALUES ({s})"
        print(quer)
        cursor.execute(quer)

    except Exception as e:
        print(e)


def db_select(cursor, table_name:list , values: list or None, condition:list = None):

    """
    Select from table. 
    INPUT:  cursor: current cursor, 
            table_name: name of the table you want to select items from
            values: the columns you want to retrieve, use ['*'] if you want all columns
            condition: the condition you want to have on you query. 
    """

    s =f'{values[0]}' 

    tn = table_name[0]

    for i in range(1, len(table_name)): 
        tn += ", " + "'"+table_name[i]+"'"

    for i in range(1, len(values)): 
        s += ", " + "'" +values[i] + "'" 

    if not condition: 

        quer = f"SELECT {s} FROM '{table_name}'"

    elif condition: 
        c = f'{condition[0]}'
        for i in range(1, len(condition)): 
            c += ", " + "'" +condition[i] + "'" 

        quer = f"SELECT {s} FROM '{tn}' WHERE {c}"
        print(quer)
        pass

    cursor.execute(quer)





    






        
