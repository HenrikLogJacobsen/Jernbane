import sqlite3
import queries as q
import user_functions as uf


con = sqlite3.connect("./db/prosjekt.db")

c = con.cursor()

#Hjelpefunksjoner
def printLines(table):
    q.db_select(c, table, '*')
    print(table)
    for row in c:
        print(row)
    print()


#Applikasjon

while True:
    s = input("Skriv inn bokstav tilhørende brukerhistorie (a/b/c/d/e/f/g/h): ")


    if (s == "a"):
        print("a) Data for Nordlandsbanen\n")
        printLines("Banestrekning")
        printLines("Stasjon")
        printLines("Delstrekning")


    elif (s == "b"):
        print("b) og f) Data for togruter på Nordlandsbanen\n")
        printLines("Togrute")
        printLines("Operator")
        printLines("RutePaStrekning")
        printLines("PaRute")
        printLines("RutePaUkedag")
        printLines("Vogn")
        printLines("Vognoppsett")
        printLines("Stol")
        printLines("Kupe")
        printLines("Seng")
        printLines("TogruteForekomst")


    elif (s == "c"):
        print("c) Søke etter togruter som er innom en stasjon en ukedag")

        stationSearch = input("Skriv inn stasjon (eks. Fauske): ")
        daySearch = input("Skriv inn ukedag (eks. onsdag): ")

        try: 
            uf.get_all_routes(c, stationSearch, daySearch)
            print("Togrute")
            for row in c:
                print(row)
            print()
        except Exception as e:
            print("En feil har oppstått:\n", e,"\nPrøv igjen")
            

    elif (s == "d"):
        print("d) Søke etter togruter som går en strekning på en gitt tid")
        startSearch = input("Skriv inn startstasjon: ")
        endSearch = input("Skriv inn sluttstasjon: ")
        dateSearch = input("Skriv inn dato (dd-mm-yyyy): ")
        timeSearch = input("Skriv inn klokkeslett (hh:mm): ")

        try:
            uf.find_route(c, startSearch, endSearch, timeSearch, dateSearch)
            print("Togrute | Forekomst-Avgangsdato | Forekomst-Avgangstid")
            for row in c:
                print(row)
            print()
        except Exception as e:
            print("En feil har oppstått:\n", e,"\nPrøv igjen")


    elif (s == "e"):
        print("e) Registrere seg i kunderegisteret")
        name = input("Skriv inn navn: ")
        email = input("Skriv inn e-post: ")
        phone = input("Skriv inn telefonnummer: ")
        try:
            uf.create_user(c, name, email, phone)
            con.commit()
        except Exception as e:
            print("En feil har oppstått:\n", e,"\nPrøv igjen")
        
    elif (s == "f"):
        print("f) Data for å håndtere billettkjøp blir vist i b)\nher er noen andre relevante tabeller")
        printLines("Kunde")
        printLines("Kundeordre")
        printLines("SengeBillett")
        printLines("SitteBillett")
    
    elif (s == "g"): 
        print("g) kjøpe en billett til en spesifik togruteforekomst. \n Nyttig tabeller")
        printLines("Kunde")
        printLines("Togruteforekomst")

        print("-----------------------------------------------------------------------------------------------")

        kunde = input("Hvilken kunde er logget inn?")
        typ = input("Hvilken type billett vil du kjøpe?")    
        dato = input("Hvilken dato vil du reise?")
        klokke = input("Hvilket klokkeslett vil du reise?")
        startStasjon = input("Hvor vil du reise fra?")
        endeStasjon = input("Hvor vil du reise til?")

        ruter = uf.find_route(c, startStasjon, endeStasjon, klokke, dato)
        
        print("Ruter du kan ta: ")
        for row in ruter:
            print(row)
        print()
        ruteID = input("Hvilken rute vil du ta? (velg en av togrute ID)")

        if typ == "seng": 
            ava = uf.available_tickets(c, "seng", dato, ruteID)

            print("Ledige sengeplasser: ")
            print("SengeNr - KupeNr - VognNr")
            for el in ava: 
                print("  ", el[0], "   |   ", el[1],"  |   ",el[2])
            
            sengeNr = [int(x) for x in input("Velg en eller flere av sengene over").split()]

            kupeNr = -1 
            vognNr = -1
            for el in ava: 
                if el[0] == sengeNr[0]: 
                    kupeNr = el[1]
                    vognNr = el[2]
                    break
            
            uf.buy_ticket_seng(c, kunde, ruteID, startStasjon, endeStasjon, klokke, dato, sengeNr, vognNr) 
            con.commit()
            print("kjøp fulført!")

        if typ == "stol": 
            ava = uf.available_tickets(c, "stol", dato, ruteID)

            print("Ledige sitteplasser: ")
            print("StolNr - VognNr - Togruteforekomst")
            for el in ava: 
                print("  ", el[0], "   |   ", el[1],"  |       ",el[2])

            vognNr = input("Velg en av vognene")
            vognNr = int(vognNr)
            stolNr = [int(x) for x in input("Velg en eller flere av stolene over tilhørende valgt vogn").split()]


            uf.buy_ticket_stol(c, kunde, ruteID, startStasjon, endeStasjon, klokke, dato, stolNr, vognNr)
            con.commit()
            print("kjøp fulført!")

        

    else:
        break

con.close()



