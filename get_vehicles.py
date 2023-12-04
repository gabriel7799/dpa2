from bson import ObjectId
from pymongo import MongoClient

from mongoengine import Document, ObjectIdField, StringField,FloatField


class Vehicle(Document):
    _id = ObjectIdField(required=True)
    type = StringField(required=False)
    model = StringField(required=False)
    brand = StringField(required=False)
    trackedDistance=FloatField(required=False)
    urbanPercentage=FloatField(required=False)
    highwayPercentage = FloatField(required=False)


class VehicleRepository:
    def __init__(self):
        self.client = MongoClient('10.20.3.130',
                                  username='admin',
                                  password='BETFfwnGZvUyFNwvHTJW',
                                  authSource='admin',
                                  authMechanism='SCRAM-SHA-256')


        self.db = self.client['fleet']
        self.collection = self.db['vehicle']

    def get_vehicle_By_Id(self, id):
        vehicle_doc = self.collection.find_one({'_id': ObjectId(id)})

        if vehicle_doc:
            vehicle_object = Vehicle(
                _id=vehicle_doc['_id'],
                type=vehicle_doc.get('type', ''),
                model=vehicle_doc.get('model', ''),
                brand=vehicle_doc.get('brand', ''),
                trackedDistance=vehicle_doc.get("statistics.trackedDistance",''),
                urbanPercentage = vehicle_doc.get("statistics.urbanPercentage", ''),
                highwayPercentage = vehicle_doc.get("statistics.highwayPercentage", '')

            )

            result_vehicle = [{
                "vehicle_data_in_fms": {
                    'id': str(vehicle_object._id),
                    'type': str(vehicle_object.type),
                    'model': str(vehicle_object.model),
                    'make': str(vehicle_object.brand),
                    'trackedDistance':str(vehicle_object.trackedDistance),
                    'urbanPercentage':str(vehicle_object.urbanPercentage),
                    'highwayPercentage': str(vehicle_object.highwayPercentage)
                }
            }]

            return result_vehicle
