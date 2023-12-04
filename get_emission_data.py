import mysql.connector
from config import sql_Client

class Emissiondata:
    def __init__(self):
        self.host = sql_Client["host"]
        self.user = sql_Client["user"],
        self.password = sql_Client["password"]
        self.db = "kba2023"

    def get_emission_data(self, hsn, tsn) -> int:
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db
        )

        try:
            with (connection.cursor() as cursor):
                sql_query = ("SELECT Co2_kombiniert,Fahrzeughersteller,Handelsname,Fahrzeugtyp,Verbrauch_kombiniert"
                             " FROM Fahrzeuge"
                             " WHERE hsn=%s"
                             " AND tsn=%s"
                             " ORDER BY Co2_kombiniert DESC"
                             " LIMIT 1")
                cursor.execute(sql_query, (hsn, tsn))

                print(cursor.statement)

                result = cursor.fetchone()

                if result is not None:
                    emissions = [{
                        "database_vin": {
                            'make': result[1],
                            'name': result[2],
                            'vehicle_type': result[3],
                            'co2_per_km_in_g': result[0],
                            'consumption_l/100km':result[4]

                        }}]

                    return emissions

                # If no results found
                print("Keine Ergebnisse gefunden.")

        except Exception as e:
            print(f"Fehler beim Verbindungsaufbau zur Datenbank: {str(e)}")

        finally:
            connection.close()
