import unittest
from datetime import date

from app import create_app, db
from app.models import User


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

    def test_delete_user_when_user_id_exists(self):
        with self.app.app_context():
            user = User(name='john', surname='smith', email='john@example.com', hash='123456', dob=date(2005, 6, 1))
            db.session.add(user)
            db.session.commit()

        response = self.client.delete('delete_user/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Status': 'OK, User 1 deleted'})

        # Check that user is no longer in the database
        with self.app.app_context():
            self.assertEqual(db.session.query(User).filter(User.id == 1).count(), 0)

    def test_delete_user_when_user_id_does_not_exist(self):
        with self.app.app_context():
            user = User(name='john', surname='smith', email='john@example.com', hash='123456', dob=date(2005, 6, 1))
            db.session.add(user)
            db.session.commit()

        response = self.client.delete('delete_user/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Error": "No User Found"})

        # Check that user 1 still exists in the database
        with self.app.app_context():
            self.assertEqual(db.session.query(User).filter(User.id == 1).count(), 1)
