import sqlite3

def db_insert(table_name: str, values: list) :

    con = sqlite3.connect("prosjekt.db")

    cursor = con.cursor()

    s = ""

    for element in values: 
        s += element + ","

    

    cursor.execute("INSERT INTO {table_name} VALUES ({s})")
    
