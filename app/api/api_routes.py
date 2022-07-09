import json

from flask import Response, make_response, jsonify, request, Blueprint

from app import db
from app.models import User, Hatch, Measurement, Sensor, Egg, Weight

api_bp = Blueprint('api', __name__)


@api_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Gets an entry from the user table"""
    user = User.query.get(user_id)
    if user is not None:
        api_response: Response = make_response(jsonify({'User': user.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@api_bp.route('/create_user', methods=['POST'])
def create_user():
    """Creates a new user"""
    data = request.json

    if all(field in data for field in ['name', 'surname', 'dob', 'email', 'hash']):

        try:
            user = User(name=data['name'],
                        surname=data['surname'],
                        dob=data['dob'],
                        email=data['email'],
                        hash=data['hash'])
            user.create()
            api_response: Response = make_response({'Status': 'OK'}, 200)
            return api_response

        except ValueError:
            return make_response({'Error': 'Bad data'})

    return make_response({'Error': request.json}, 200)


@api_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id) -> Response:
    """Deletes a user from the database"""
    if db.session.query(User).filter(User.id == user_id).count() == 0:
        api_response = make_response({'Error': 'No User Found'})
        return api_response

    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    # Check record was successfully deleted
    if db.session.query(User).filter(User.id == user_id).count() == 0:
        api_response = make_response({'Status': 'OK, User ' + str(user_id) + ' deleted'})
    else:
        api_response = make_response({'Status': 'Transaction Error'})

    return api_response


@api_bp.route('/hatch/<int:hatch_id>', methods=['GET'])
def get_hatch(hatch_id):
    """Gets an entry from the hatch table"""
    hatch = Hatch.query.get(hatch_id)
    if hatch is not None:
        api_response: Response = make_response(jsonify({'Hatch': hatch.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@api_bp.route('/create_hatch', methods=['POST'])
def create_hatch():
    """Creates a new hatch"""
    data = request.json

    if all(field in data for field in ['user_id', 'sensor_id', 'start_date', 'is_active']):

        try:
            hatch = Hatch(user_id=data['user_id'],
                          sensor_id=data['sensor_id'],
                          start_date=data['start_date'],
                          is_active=data['is_active'])
            hatch.create()
            api_response: Response = make_response({'Status': 'OK'})
            return api_response

        except ValueError:
            return make_response({'Error': 'Bad data'})

    return make_response({'Error': request.json}, 200)


@api_bp.route('/egg/<int:egg_id>', methods=['GET'])
def get_egg(egg_id):
    """Gets an entry from the egg table"""
    egg = Egg.query.get(egg_id)
    if egg is not None:
        api_response: Response = make_response(jsonify({'Egg': egg.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@api_bp.route('/create_egg', methods=['POST'])
def create_egg():
    """Creates a new egg"""
    data = request.json

    if all(field in data for field in ['hatch_id', 'start_date']):

        try:
            egg = Egg(hatch_id=data['hatch_id'],
                      start_date=data['start_date'],
                      end_date=None,
                      hatched=False)

            egg.create()
            api_response: Response = make_response({'Status': 'OK'})
            return api_response

        except ValueError:
            return make_response({'Error': 'Bad data'})

    return make_response({'Error': request.json}, 200)


@api_bp.route('/weight/<int:weight_id>', methods=['GET'])
def get_weight(weight_id):
    """Gets an entry from the weight table"""
    weight = Weight.query.get(weight_id)
    if weight is not None:
        api_response: Response = make_response(jsonify({'Weight': weight.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@api_bp.route('/log_weight', methods=['POST'])
def log_weight():
    """Creates a new weight entry"""
    data = request.json

    if all(field in data for field in ['egg_id', 'date_time', 'weight']):

        try:
            weight = Weight(egg_id=data['egg_id'],
                            date_time=data['date_time'],
                            weight=data['weight'])
            weight.create()
            api_response: Response = make_response({'Status': 'OK'})
            return api_response

        except ValueError:
            return make_response({'Error': 'Bad data'})

    return make_response({'Error': request.json}, 200)


@api_bp.route('/measurement/<int:measurement_id>', methods=['GET'])
def get_measurement(measurement_id):
    """Gets an entry from the measurement table"""
    measurement = Measurement.query.get(measurement_id)
    if measurement is not None:
        api_response: Response = make_response(jsonify({'Measurement': measurement.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@api_bp.route('/log_measurement', methods=['POST'])
def log_measurement():
    """Logs a new reading from a sensor"""
    data = request.json

    if all(field in data for field in ['sensor_id', 'date_time', 'temperature', 'humidity']):

        try:
            measurement = Measurement(sensor_id=data['sensor_id'],
                                      date_time=data['date_time'],
                                      temperature=data['temperature'],
                                      humidity=data['humidity'])
            measurement.create()
            api_response: Response = make_response({'Status': 'OK'})
            return api_response

        except ValueError:
            return make_response({'Error': 'Bad data'})

    return make_response({'Error': request.json}, 200)


@api_bp.route('/sensor/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    """Gets an entry from the sensor table"""
    sensor = Sensor.query.get(sensor_id)
    if sensor is not None:
        api_response: Response = make_response(jsonify({'Sensor': sensor.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response
