from flask import Flask, jsonify
from flask_cors import CORS

from get_tracks import TrackRepository
from get_vehicles import VehicleRepository
from get_emission_data import Emissiondata
from calculation_co2 import calculate_co2_on_time

app = Flask(__name__)
CORS(app)


@app.route('/data/<vehicle_id>', methods=['GET'])
def get_data(vehicle_id):
    track_repo = TrackRepository()
    track_result = track_repo.get_total_distance_calculated(vehicle_id)

    vehicle_repo = VehicleRepository()
    vehicle_instance = vehicle_repo.get_vehicle_By_Id(vehicle_id)

    result = vehicle_instance + track_result

    return jsonify(result)


@app.route("/data/<vehicle_id>/<hsn_tsn>", methods=['GET'])
def calculate_emissions(vehicle_id, hsn_tsn):
    track_repo = TrackRepository()
    track_result = track_repo.get_total_distance_calculated(vehicle_id)

    vehicle_repo = VehicleRepository()
    vehicle_instance = vehicle_repo.get_vehicle_By_Id(vehicle_id)

    hsn = hsn_tsn[0:4]
    tsn = hsn_tsn[4:7]

    emission = Emissiondata()
    emission_result = emission.get_emission_data(hsn, tsn)

    daily_co2 = calculate_co2_on_time(track_result, emission_result)

    result = vehicle_instance + emission_result + track_result + daily_co2

    return jsonify(result)


app.run()
