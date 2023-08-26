from unittest import TestCase
from app import app
from flask import session
from models import db , USER , QRC_IMAGES_DB


class QRCodeTestCases(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a testing database
        app.config['WTF_CSRF_ENABLED'] = False

        with app.app_context():
            db.create_all()

