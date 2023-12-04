import mysql.connector
from tqdm import tqdm
def load_db(data):
    #Bestätigungsprompt für das Einlesen in die Datenbank
    user_input = input("Wollen Sie den Dataframe in die Datenbank laden?, drücken Sie Enter um fortzufahren")
    while user_input != "":
        user_input = input("Press enter to continue: ")

    # Verbindung zur Datenbank herstellen
    connection = mysql.connector.connect(host='localhost',
                                         user='Daniel',
                                         password='12345',
                                         db='kba2023')
    print("Verbindung zur Datenbank hergestellt")

    # SQL-Befehl zum Einfügen der Daten in die Tabelle erstellen
    create_table_sql = ('CREATE TABLE IF NOT EXISTS Fahrzeuge ('
                        'id int primary key AUTO_INCREMENT,'
                        'HSN CHAR(4) NOT NULL,'
                        'TSN CHAR(3) NOT NULL,'
                        'Fahrzeughersteller VARCHAR(100) ,'     
                        'Fahrzeugklasse VARCHAR(4),'
                        'Handelsname VARCHAR(100) ,'
                        'Fahrzeugtyp CHAR(3),'
                        'Kraftstoffcode CHAR(4),'
                        'Leistung FLOAT,'
                        'Emissionscode CHAR(4) ,'
                        'Co2_kombiniert FLOAT NOT NULL,'
                        'Co2_gewichtet FLOAT ,'
                        'Co2_kombiniert2 FLOAT,'
                        'Co2_gewichtet2 FLOAT ,'
                        'Verbrauch_kombiniert FLOAT	, '
                        'Verbrauch_gewichtet FLOAT , '
                        'Verbrauch_kombiniert2 FLOAT , '
                        'Verbrauch_gewichtet2 FLOAT)ENGINE=InnoDB;')

    try:
        with connection.cursor() as cursor:
            # SQL-Befehl ausführen

            cursor.execute(create_table_sql)

        # Änderungen speichern
        connection.commit()
        print("Tabelle erfolgreich erstellt!")

    except Exception as e:
        print(f"Fehler beim Einfügen der Daten: {str(e)}")

    print(f"Dataframe wird in die Datenbank geladen")

    total_rows = len(data)
    # Schleife über die Zeilen des DataFrames
    for index, row in tqdm(data.iterrows(), total=total_rows):
        #es werden %s-Platzhalter für den SQL-Befehl verwendet
        insert_data_sql = (
            "INSERT INTO Fahrzeuge (HSN,TSN,Fahrzeughersteller,Fahrzeugklasse,Handelsname,Fahrzeugtyp,Kraftstoffcode,Leistung,Emissionscode,"
            "Co2_kombiniert,Co2_gewichtet,Co2_kombiniert2,Co2_gewichtet2,Verbrauch_kombiniert,Verbrauch_gewichtet,Verbrauch_kombiniert2,"
            "Verbrauch_gewichtet2) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        # Werte für die Platzhalter im SQL-Befehl festlegen (abhängig von den Spaltennamen und -reihenfolgen),die mit dem dataframe korrespondieren
        values = (row['HSN'],
                  row['TSN'],
                  row['Fahrzeughersteller'],
                  row["Fahrzeugklasse"],
                  row['Handelsname'],
                  row["Fahrzeugtyp"],
                  row["Kraftstoffcode"],
                  row["Leistung"],
                  row["Emissionscode"],
                  row["Co2_kombiniert"],
                  row["Co2_gewichtet"],
                  row["Co2_kombiniert2"],
                  row["Co2_gewichtet2"],
                  row["Verbrauch_kombiniert"],
                  row["Verbrauch_gewichtet"],
                  row["Verbrauch_kombiniert2"],
                  row["Verbrauch_gewichtet2"],

                  )

        try:
            with connection.cursor() as cursor:
                # SQL-Befehl ausführen
                cursor.execute(insert_data_sql, values)

            # Änderungen speichern
            connection.commit()



        except Exception as e:
            print(f"Fehler beim Einfügen der Daten: {str(e)}")

    # Verbindung schließen
    connection.close()
