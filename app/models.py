from datetime import date

from . import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    dob = db.Column(db.String(50))
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
    date_time = db.Column(db.String(50))
    m_type = db.Column(db.String(50))
    measurement = db.Column(db.Float)

    def create(self) -> None:
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, sensor_id, date_time, m_type, measurement):
        self.sensor_id = sensor_id
        self.date_time = date_time
        self.m_type = m_type
        self.measurement = measurement

    def json(self) -> dict:
        """return JSON formatted data"""
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'datetime': self.date_time,
            'm_type': self.m_type,
            'measurement': self.measurement
        }


class Hatch(db.Model):
    __tablename__ = "hatch"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    sensor_id = db.Column(db.Integer)
    start_date = db.Column(db.String(50))
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
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
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
    date_time = db.Column(db.String(50))
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

