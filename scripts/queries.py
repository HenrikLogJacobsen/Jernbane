import sqlite3

def db_insert(cursor , table_name: str, values: list) :

    s = "'"+values[0]+"'"

    for i in range(1, len(values)): 
        s += ", " + "'" +values[i]+"'" 

    
    quer = f"INSERT INTO '{table_name}' VALUES ({s})"
    print(quer)
    cursor.execute(quer)



    
