"""
BaseTest

This class should be the parent class to each unit test.
It allows for instantiation of the database dynamically,
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db
import os


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    ADMIN="adm1,adm2"
    UPLOADED_FILES_DEST = os.path.join("static", "files") 

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = BaseTest.SQLALCHEMY_DATABASE_URI
        app.config['ADMIN'] = BaseTest.ADMIN
        app.config['UPLOADED_FILES_DEST'] = BaseTest.UPLOADED_FILES_DEST

        with app.app_context():
            db.init_app(app)
            db.create_all()
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
