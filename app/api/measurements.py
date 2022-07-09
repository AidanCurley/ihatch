from datetime import datetime

from flask import request, jsonify, make_response, Response
from . import api
from ..models import Measurement


@api.route('/measurement/<int:measurement_id>', methods=['GET'])
def get_measurement(measurement_id):
    """Gets an entry from the measurement table"""
    measurement = Measurement.query.get(measurement_id)
    if measurement is not None:
        api_response: Response = make_response(jsonify({'Measurement': measurement.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@api.route('/log_measurement', methods=['POST'])
def log_measurement():
    """Logs a new reading from a sensor"""
    data = request.json

    if all(field in data for field in ['sensor_id', 'date_time', 'temperature', 'humidity']):

        try:
            measurement = Measurement(sensor_id=data['sensor_id'],
                                      date_time=datetime.strptime(data['date_time'], '%Y-%m-%dT%H:%M:%S'),
                                      temperature=data['temperature'],
                                      humidity=data['humidity'])
            measurement.create()
            api_response: Response = make_response({'Status': 'OK'})
            return api_response

        except ValueError:
            return make_response({'Error': 'Bad data'})

    return make_response({'Error': request.json}, 200)