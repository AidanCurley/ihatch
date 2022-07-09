import unittest
from datetime import date, datetime

from app import create_app, db
from app.models import User, Sensor, Egg, Hatch, Weight, Measurement


class APIGetRequestsCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_404(self):
        response = self.client.get(
            '/wrong/url')
        self.assertEqual(response.status_code, 404)

    def test_get_user_when_user_id_exists(self):
        # add test data to the database
        with self.app.app_context():
            user = User(name='john', surname='smith', email='john@example.com', hash='123456', dob=date(2005, 6, 1))
            db.session.add(user)
            db.session.commit()

        expected_user = {'User': {'dob': 'Wed, 01 Jun 2005 00:00:00 GMT',
                                  'email': 'john@example.com', 'hash': '123456',
                                  'id': 1, 'name': 'john', 'surname': 'smith'}}
        # issue a request
        response = self.client.get('/user/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_user)

    def test_get_user_when_user_id_does_not_exist(self):
        # add test data to the database
        with self.app.app_context():
            user = User(name='john', surname='smith', email='john@example.com', hash='123456', dob=date(2005, 6, 1))
            db.session.add(user)
            db.session.commit()

        expected_data = {'Error': 'No result'}

        response = self.client.get('/user/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_sensor_when_sensor_id_exists(self):
        with self.app.app_context():
            sensor = Sensor(user_id=1, is_connected=True)
            db.session.add(sensor)
            db.session.commit()

        expected_sensor = {'Sensor': {'id': 1, 'is_connected': True, 'user_id': 1}}

        response = self.client.get('/sensor/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_sensor)

    def test_get_sensor_when_sensor_id_does_not_exist(self):
        with self.app.app_context():
            sensor = Sensor(user_id=1, is_connected=True)
            db.session.add(sensor)
            db.session.commit()

        expected_data = {'Error': 'No result'}

        response = self.client.get('/sensor/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_hatch_when_hatch_id_exists(self):
        with self.app.app_context():
            hatch = Hatch(user_id=1, sensor_id=1, is_active=True, start_date=date(2022, 1, 1))
            db.session.add(hatch)
            db.session.commit()

        expected_hatch = {'Hatch': {'id': 1, 'is_active': True,
                                    'sensor_id': 1,
                                    'start_date': 'Sat, 01 Jan 2022 00:00:00 GMT',
                                    'user_id': 1}}

        response = self.client.get('/hatch/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_hatch)

    def test_get_hatch_when_hatch_id_does_not_exist(self):
        with self.app.app_context():
            hatch = Hatch(user_id=1, sensor_id=1, is_active=True, start_date=date(2022, 1, 1))
            db.session.add(hatch)
            db.session.commit()

        expected_data = {'Error': 'No result'}

        response = self.client.get('/hatch/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_egg_when_egg_id_exists(self):
        with self.app.app_context():
            egg = Egg(hatch_id=1, start_date=date(2022, 6, 1), end_date=None, hatched=False)
            db.session.add(egg)
            db.session.commit()

        expected_egg = {'Egg': {'end_date': None,
                                'hatch_id': 1,
                                'hatched': False,
                                'id': 1,
                                'start_date': 'Wed, 01 Jun 2022 00:00:00 GMT'}}

        response = self.client.get('/egg/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_egg)

    def test_get_egg_when_egg_id_does_not_exist(self):
        with self.app.app_context():
            egg = Egg(hatch_id=1, start_date=date(2022, 6, 1), end_date=None, hatched=False)
            db.session.add(egg)
            db.session.commit()

        expected_data = {'Error': 'No result'}

        response = self.client.get('/egg/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_weight_when_weight_id_exists(self):
        with self.app.app_context():
            weight = Weight(egg_id='john', date_time=datetime(2022, 6, 1), weight=12.2)
            db.session.add(weight)
            db.session.commit()

        expected_weight = {'Weight': {'date_time': 'Wed, 01 Jun 2022 00:00:00 GMT',
                                      'egg_id': 'john',
                                      'id': 1,
                                      'weight': 12.2}}

        response = self.client.get('/weight/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_weight)

    def test_get_weight_when_weight_id_does_not_exist(self):
        with self.app.app_context():
            weight = Weight(egg_id='john', date_time=datetime(2022, 6, 1), weight=12.2)
            db.session.add(weight)
            db.session.commit()

        expected_data = {'Error': 'No result'}

        response = self.client.get('/weight/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_measurement_when_measurement_exists(self):
        with self.app.app_context():
            measurement = Measurement(sensor_id=1, date_time=datetime(2022, 6, 1), temperature=12.2, humidity=40.25)
            db.session.add(measurement)
            db.session.commit()

        expected_measurement = {'Measurement': {'datetime': 'Wed, 01 Jun 2022 00:00:00 GMT',
                                                'humidity': 40.25,
                                                'id': 1,
                                                'sensor_id': 1,
                                                'temperature': 12.2}}

        response = self.client.get('/measurement/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_measurement)

    def test_get_measurement_when_measurement_id_does_not_exist(self):
        with self.app.app_context():
            measurement = Measurement(sensor_id=1, date_time=datetime(2022, 6, 1), temperature=12.2, humidity=40.25)
            db.session.add(measurement)
            db.session.commit()

        expected_data = {'Error': 'No result'}

        response = self.client.get('/measurement/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)
