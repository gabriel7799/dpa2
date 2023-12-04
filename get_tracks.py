from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId
from mongoengine import connect, Document, ObjectIdField, DateTimeField, FloatField


class Track(Document):
    vehicleId = ObjectIdField(required=True)
    ended = DateTimeField(required=True)
    distanceCalculated = FloatField(required=True)


class TrackRepository:
    def __init__(self):
        self.last_track = None
        self.last_day=None
        self.last_week= None
        self.last_month=None
        self.last_year= None
        self.client = MongoClient('10.20.3.130',
                                  username='admin',
                                  password='BETFfwnGZvUyFNwvHTJW',
                                  authSource='admin',
                                  authMechanism='SCRAM-SHA-256')
        self.db = self.client['fleet']
        self.collection = self.db['track']

    def get_total_distance_calculated(self, vehicle_id):
        timeframes = [1, 7, 30, 365]
        result=[]

        for timeframe in timeframes:
            end_date = datetime.datetime(2023, 11, 6)
            start_date = end_date - datetime.timedelta(days=timeframe)

            pipeline = [
                {
                    "$match": {
                        "vehicleId": ObjectId(vehicle_id),
                        "ended": {"$gte": start_date, "$lt": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total_distance_calculated": {"$sum": "$distanceCalculated"}
                    }
                }
            ]

            data_aggregation_result = self.collection.aggregate(pipeline)

            total_distance_calculated = sum([item['total_distance_calculated'] for item in data_aggregation_result])

            result.append(total_distance_calculated/1000)
            result = [round(num, 3) for num in result]


        self.last_day,self.last_week,self.last_month,self.last_year=result

        self.last_track = self.collection.find_one(
            {"vehicleId": ObjectId(vehicle_id)},
            projection={"distanceCalculated": True},
            sort=[("ended", -1)]
        )
        self.last_track=round(self.last_track["distanceCalculated"]/1000,3)

        result_tracks = [{
            "tracks": {
                "last_track_in_km": self.last_track,
                **{f"total_distance_in_{timeframes[i]}_days_in_km": result[i] for i in range(len(timeframes))}
            }
        }]

        return result_tracks
