def calculate_co2_on_time(track_result, emission_result):
    co2_last_track = float(track_result[0]['tracks']['last_track_in_km']) * emission_result[0]['database_vin'][
        'co2_per_km_in_g'] / 1000

    co2_last_day = float(track_result[0]['tracks']['total_distance_in_1_days_in_km']) * \
                   emission_result[0]['database_vin'][
                       'co2_per_km_in_g'] / 1000

    co2_last_week = float(track_result[0]['tracks']['total_distance_in_7_days_in_km']) * \
                    emission_result[0]['database_vin'][
                        'co2_per_km_in_g'] / 1000

    co2_last_month = float(track_result[0]['tracks']['total_distance_in_30_days_in_km']) * \
                     emission_result[0]['database_vin'][
                         'co2_per_km_in_g'] / 1000

    co2_last_year = float(track_result[0]['tracks']['total_distance_in_365_days_in_km']) * \
                    emission_result[0]['database_vin'][
                        'co2_per_km_in_g'] / 1000

    daily_co2 = [{
        "co2_data": {
            'co2_per_km_in_kg': round((emission_result[0]['database_vin']['co2_per_km_in_g'] / 1000), 3),
            'co2_last_track_in_kg': round(co2_last_track, 3),
            'co2_last_day_in_kg': round(co2_last_day, 3),
            'co2_last_week_in_kg': round(co2_last_week, 3),
            'co2_last_month_in_kg': round(co2_last_month, 3),
            'co2_last_year_in_kg': round(co2_last_year, 3)
        }
    }]
    return daily_co2
