import unittest
from datetime import date, datetime

from app import create_app, db
from app.models import User, Egg, Hatch, Weight, Measurement


class APIPostRequestsCase(unittest.TestCase):
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

    def test_post_404(self):
        response = self.client.post(
            '/wrong/url')
        self.assertEqual(response.status_code, 404)

    def test_create_user_with_valid_parameters(self):
        with self.app.app_context():
            user = User(name='john', surname='smith', email='john@example.com', hash='123456', dob=date(2005, 6, 1))

        response = self.client.post('/create_user', json={
            "name": "Billy",
            "surname": "NoMates",
            "dob": "1980-01-01",
            "email": "billy@friendless.com",
            "hash": "nomates"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Status': 'OK'})

        # Check that user has been inserted in the database
        with self.app.app_context():
            self.assertEqual(db.session.query(User).filter(User.email == "billy@friendless.com").count(), 1)

    def test_create_hatch_with_valid_parameters(self):
        with self.app.app_context():
            hatch = Hatch(user_id=1, sensor_id=1, is_active=True, start_date=date(2022, 1, 1))

        response = self.client.post('/create_hatch', json={
            'is_active': True,
            'sensor_id': 1,
            'start_date': 'Sat, 01 Jan 2022 00:00:00 GMT',
            'user_id': 1
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Status': 'OK'})

        # Check that hatch has been inserted in the database
        with self.app.app_context():
            self.assertEqual(db.session.query(Hatch).filter(Hatch.start_date == 'Sat, 01 Jan 2022 00:00:00 GMT').count(), 1)

    def test_create_egg_with_valid_parameters(self):
        with self.app.app_context():
            egg = Egg(hatch_id=1, start_date=date(2022, 6, 1), end_date=None, hatched=False)

        response = self.client.post('/create_egg', json={'end_date': None,
                                                         'hatch_id': 1,
                                                         'hatched': False,
                                                         'id': 1,
                                                         'start_date': 'Wed, 01 Jun 2022 00:00:00 GMT'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Status': 'OK'})

        # Check that egg has been inserted in the database
        with self.app.app_context():
            self.assertEqual(db.session.query(Egg).filter(Egg.start_date == 'Wed, 01 Jun 2022 00:00:00 GMT').count(), 1)

    def test_log_weight_with_valid_parameters(self):
        with self.app.app_context():
            weight = Weight(egg_id='john', date_time=datetime(2022, 6, 1), weight=12.2)

        response = self.client.post('/log_weight', json={'date_time': 'Wed, 01 Jun 2022 00:00:00 GMT',
                                                         'egg_id': 'john',
                                                         'id': 1,
                                                         'weight': 12.2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Status': 'OK'})

        # Check that weight has been inserted in the database
        with self.app.app_context():
            self.assertEqual(db.session.query(Weight).filter(Weight.date_time == 'Wed, 01 Jun 2022 00:00:00 GMT').count(), 1)

    def test_log_measurement_with_valid_parameters(self):
        with self.app.app_context():
            measurement = Measurement(sensor_id=1, date_time=datetime(2022, 6, 1), temperature=12.2, humidity=40.25)

        response = self.client.post('/log_measurement', json={
            "sensor_id": 3,
            "date_time": "2022-07-07T15:09:30",
            "temperature": 41.3,
            "humidity": 40
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Status': 'OK'})

        # Check that measurement has been inserted in the database
        with self.app.app_context():
            self.assertEqual(db.session.query(Measurement).filter(Measurement.date_time == '2022-07-07T15:09:30').count(), 1)