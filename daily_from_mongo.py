from datetime import datetime, timedelta
from tqdm import tqdm
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
from pymongo import MongoClient
from config import mongoConfig


class TrackRepository:
    def __init__(self, vehicle_id):
        self.client = MongoClient(mongoConfig['host'],
                                  username=mongoConfig['username'],
                                  password=mongoConfig['password'],
                                  authSource=mongoConfig['authSource'],
                                  authMechanism=mongoConfig['authMechanism'])

        self.db = self.client['fleet']
        self.collection = self.db['track']
        self.vehicle_id = vehicle_id
        self.dates = []
        self.distances = []

    def get_total_distance_calculated(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime.now().replace(hour=0, minute=0)

        for _ in tqdm(range((end_date - start_date).days + 1), desc='Progress'):
            pipeline = [
                {
                    "$match": {
                        "vehicleId": ObjectId(vehicle_id),
                        "ended": {"$gte": start_date, "$lt": start_date + timedelta(days=1)}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total_distance_calculated": {"$sum": "$distanceCalculated"}
                    }
                }
            ]

            daily_value = list(self.collection.aggregate(pipeline))

            if len(daily_value) > 0 and daily_value[0]['total_distance_calculated'] != 0:
                self.dates.append(start_date.strftime('%Y-%m-%d'))
                self.distances.append(float(round(daily_value[0]['total_distance_calculated'] / 1000)))

            start_date += timedelta(days=1)

    def plot(self):
        # Plotting the data using matplotlib
        plt.figure(figsize=(20, 5))
        plt.plot(self.dates, self.distances, 'o-', color="orange")
        plt.title(f'Fahrstrecken pro Tag für vehicleID:{vehicle_id}', fontsize=20)
        plt.xlabel('Datum', fontsize=16)
        plt.ylabel('Strecke pro Tag in km', fontsize=20)

        # Show only every 10th x-label without overlapping
        every_nth_label = 20
        for n, label in enumerate(plt.gca().xaxis.get_ticklabels()):
            if n % every_nth_label != 0:
                label.set_visible(False)
            else:
                label.set_fontsize(10)

        plt.show()


vehicle_id = "60cda6416a68e6e0e43e8129"
repository = TrackRepository(vehicle_id)
repository.get_total_distance_calculated()
repository.plot()
