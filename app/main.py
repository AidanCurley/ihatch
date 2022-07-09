"""Launch the application"""
from flask import request, jsonify, make_response, Response, render_template

from app import create_app, db
from app.models import User, Sensor, Hatch, Egg, Weight

app = create_app('development')



@app.route('/')
def landing_page():
    """Controller for the landing page route"""
    return render_template('landing.html')


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Gets an entry from the user table"""
    user = User.query.get(user_id)
    if user is not None:
        api_response: Response = make_response(jsonify({'User': user.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@app.route('/sensor/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    """Gets an entry from the sensor table"""
    sensor = Sensor.query.get(sensor_id)
    if sensor is not None:
        api_response: Response = make_response(jsonify({'Sensor': sensor.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@app.route('/hatch/<int:hatch_id>', methods=['GET'])
def get_hatch(hatch_id):
    """Gets an entry from the hatch table"""
    hatch = Hatch.query.get(hatch_id)
    if hatch is not None:
        api_response: Response = make_response(jsonify({'Hatch': hatch.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@app.route('/egg/<int:egg_id>', methods=['GET'])
def get_egg(egg_id):
    """Gets an entry from the egg table"""
    egg = Egg.query.get(egg_id)
    if egg is not None:
        api_response: Response = make_response(jsonify({'Egg': egg.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@app.route('/weight/<int:weight_id>', methods=['GET'])
def get_weight(weight_id):
    """Gets an entry from the weight table"""
    weight = Weight.query.get(weight_id)
    if weight is not None:
        api_response: Response = make_response(jsonify({'Weight': weight.json()}), 200)
    else:
        api_response: Response = make_response({'Error': 'No result'}, 200)

    return api_response


@app.route('/create_user', methods=['POST'])
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
            api_response: Response = make_response({'Status': 'OK'})
            return api_response

        except ValueError:
            return make_response({'Error': 'Bad data'})

    return make_response({'Error': request.json}, 200)


@app.route('/create_hatch', methods=['POST'])
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


@app.route('/create_egg', methods=['POST'])
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


@app.route('/create_weight', methods=['POST'])
def create_weight():
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


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
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


if __name__ == "__main__":
    app.run(debug=True)
