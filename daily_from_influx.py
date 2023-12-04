from datetime import datetime, timedelta
from pprint import pprint
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient
from tqdm import tqdm
from regression import linear_regression
from config import INFLUX_TOKEN


class Fuelrepository:
    def __init__(self, vehicle_id):
        self.token = INFLUX_TOKEN
        self.vehicle_id = vehicle_id
        self.end_value = None
        self.co2_values = None
        self.start_value = None
        self.timestamps_dt = None
        self.values_adjusted = None
        self.values_day = []
        self.dict_daily={}

    def query_influxdb_for_year(self):

        org = "cynatix"
        url = "http://localhost:8086"

        # Verbindung zur Datenbank herstellen
        client = InfluxDBClient(url=url, token=self.token)

        # Startdatum und Enddatum festlegen
        start_date = datetime(2023, 1, 1)
        end_date = datetime.now().replace(hour=0, minute=0, second=0)


        # Variable für den Wert des Vortages in der Schleife zum Abgleich auf Nullwerte
        previous_value = None

        for _ in tqdm(range((end_date - start_date).days + 1), desc='Progress'):
            # Query-String für die Abfrage erstellen
            query_string = (
                f'from(bucket: "track-record-processing") '
                f'|> range(start: {start_date.strftime("%Y-%m-%dT00:00:00Z")}, stop:{start_date.strftime("%Y-%m-%dT23:59:59Z")}) '
                f'|> filter(fn:(r) => r["_measurement"] == "sensor-value") '
                f'|> filter(fn:(r) => r["vehicleId"] == "{self.vehicle_id}")'
                f'|> filter(fn:(r) => r["_field"] == "FMS_ENGINE_TOTAL_FUEL_USED")'
                f'|> aggregateWindow(every: 24h, fn: max, createEmpty:false)'
                f'|> yield(name:"yield")'
                # 24h für tägliches Zeitfenster,max-Werte da wir fohrtwährend einen steigenden Wert haben und den größten Wert zum ende des Tages auslesen wollen
            )

            tables = client.query_api().query(query=query_string, org="cynatix")

            for table in tables:
                for record in table.records:
                    current_value = record.values['_value']

                    if current_value != previous_value:
                        self.dict_daily[str(record.get_time())] = current_value

                    previous_value = current_value

            start_date += timedelta(days=1)

        return self.dict_daily

    def calculate(self):

        timestamps = list(self.dict_daily.keys())
        values_fuel = list(self.dict_daily.values())
        # Errechnen von Co2-Emission aus dem Kraftstoffverbrauch mit Emissionfaktor 2.37 für Benzin
        self.co2_values = []
        for i in range(0, len(values_fuel)):
            co2_daily = values_fuel[i] * 2.37
            self.co2_values.append(co2_daily)

        # Den Startwert setzen und alle anderen Werte um den Startwert subtrahieren
        start_value = self.co2_values[0]
        self.values_adjusted = [values - start_value for values in self.co2_values]
        pprint(self.values_adjusted)

        # Täglichen Verbrauch berechnen

        for i in range(1, len(self.values_adjusted)):
            daily_consumption = self.co2_values[i] - self.co2_values[i - 1]
            self.values_day.append(daily_consumption)

        # Die Zeitstempel in ein geeignetes Format für die Visualisierung konvertieren (z.B. Datetime)
        self.timestamps_dt = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S%z') for ts in timestamps]

        #Emission für das gesamte Jahr mithilfe linearer Regression ermitteln
        self.end_value = linear_regression(self.timestamps_dt, self.values_adjusted)

    def plot(self):
        fig, ax1 = plt.subplots(figsize=(20, 5))
        background_color = '#ECF0F1'

        # Erstellen der skaleafür die Gesamtemission
        fig.patch.set_facecolor(background_color)
        color = 'tab:blue'
        ax1.set_xlabel('Datum', fontsize=20)  # Größere Schrift für x-Achse
        ax1.set_ylabel('Gesamtemission Co2 in kg', color=color,
                       fontsize=20)  # Größere Schrift für y-Achse und Farbe festlegen
        ax1.plot(self.timestamps_dt + [datetime(datetime.now().year, 12, 31)], self.values_adjusted + [self.end_value],
                 label='Historische Daten', color=color)

        ax1.tick_params(axis='y', labelcolor=color, labelsize=16)

        # Hinzufügen des Bereichs für die Vorhersage
        prediction_start_date = self.timestamps_dt[-1]
        prediction_end_date = datetime(datetime.now().year, 12, 31)
        plt.fill_between([prediction_start_date, prediction_end_date], self.end_value, alpha=0.3, color='orange',
                         label='Vorhersage')

        # Vorhersage als Text ausgeben und positionieren
        plt.text(prediction_end_date - timedelta(days=1), self.end_value / 2, f'Vorhersage: {self.end_value:.2f} kg',
                 ha='right',
                 fontsize=14)

        # Zweite Skala auf der rechten Seite einführen für tägliche Emission
        ax2 = ax1.twinx()
        color_daily_emission = 'tab:orange'
        ax2.set_ylabel('Tägliche Emission Co2 in kg', color=color_daily_emission, fontsize=20)
        ax2.tick_params(axis='y', labelcolor=color_daily_emission, labelsize=16)
        ax2.plot(self.timestamps_dt[1:], self.values_day[0:], marker='o', linestyle='-', markersize=6,
                 label='_nolegend_',
                 color=color_daily_emission)

        year = datetime.now().year
        fig.suptitle(
            f'Co2-Emissionen {year} für vehicleId:{self.vehicle_id} mit Vorhersage für die Emisionen des gesamten Jahres',
            fontsize=20)
        fig.tight_layout()

        plt.show()


vehicle_id = "60cda6416a68e6e0e43e8129"
repository = Fuelrepository(vehicle_id)
dict_daily = repository.query_influxdb_for_year()
repository.calculate()
repository.plot()

