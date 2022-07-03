"""Launch the application"""
import os
from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, request, jsonify, make_response, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

load_dotenv()

app = Flask(__name__)

# csrf = CSRFProtect()
# csrf.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['WTF_CSRF_SECRET_KEY'] = os.getenv("WTF_CSRF_SECRET_KEY")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    dob = db.Column(db.Date)
    email = db.Column(db.String(50))
    hash = db.Column(db.String(100))

    def create(self) -> None:
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, surname, dob, email, hash):
        self.name = name
        self.surname = surname
        self.dob = dob
        self.email = email
        self.hash = hash

    def json(self) -> dict:
        """return JSON formatted data"""
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'dob': self.dob,
            'email': self.email,
            'hash': self.hash
        }


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    is_connected = db.Column(db.Boolean)

    def create(self) -> None:
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, user_id, is_connected):
        self.user_id = user_id
        self.is_connected = is_connected

    def json(self) -> dict:
        """return JSON formatted data"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'is_connected': self.is_connected
        }


class Measurement(db.Model):
    __tablename__ = "measurement"
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

    def create(self) -> None:
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, sensor_id, date_time, temperature, humidity):
        self.sensor_id = sensor_id
        self.date_time = date_time
        self.temperature = temperature
        self.humidity = humidity

    def json(self) -> dict:
        """return JSON formatted data"""
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'datetime': self.date_time,
            'temperature': self.temperature,
            'humidity': self.humidity
        }


class Hatch(db.Model):
    __tablename__ = "hatch"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    sensor_id = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean)

    def create(self) -> None:
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, user_id, sensor_id, start_date, is_active):
        self.user_id = user_id
        self.sensor_id = sensor_id
        self.start_date = start_date
        self.is_active = is_active

    def json(self) -> dict:
        """return JSON formatted data"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sensor_id': self.sensor_id,
            'start_date': self.start_date,
            'is_active': self.is_active
        }


class Egg(db.Model):
    __tablename__ = "egg"
    id = db.Column(db.Integer, primary_key=True)
    hatch_id = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    hatched = db.Column(db.Boolean)

    def create(self) -> None:
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, hatch_id, start_date, end_date, hatched):
        self.hatch_id = hatch_id
        self.start_date = start_date
        self.end_date = end_date
        self.hatched = hatched

    def json(self) -> dict:
        """return JSON formatted data"""
        return {
            'id': self.id,
            'hatch_id': self.hatch_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'hatched': self.hatched
        }


class Weight(db.Model):
    __tablename__ = "weight"
    id = db.Column(db.Integer, primary_key=True)
    egg_id = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)
    weight = db.Column(db.Float)

    def create(self) -> None:
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, egg_id, date_time, weight):
        self.egg_id = egg_id
        self.date_time = date_time
        self.weight = weight

    def json(self) -> dict:
        """return JSON formatted data"""
        return {
            'id': self.id,
            'egg_id': self.egg_id,
            'date_time': self.date_time,
            'weight': self.weight
        }


db.create_all()


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


@app.route('/measurement/<int:measurement_id>', methods=['GET'])
def get_measurement(measurement_id):
    """Gets an entry from the measurement table"""
    measurement = Measurement.query.get(measurement_id)
    if measurement is not None:
        api_response: Response = make_response(jsonify({'Measurement': measurement.json()}), 200)
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


@app.route('/log_measurement', methods=['POST'])
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


if __name__ == "__main__":
    app.run(debug=True)
