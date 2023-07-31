import unittest
import db
from api import app
import os
import json
os.environ["DATABASE_URL"] = "sqlite://"


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        db.create_tables()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_tables()
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None

    def test_app(self):
        assert self.app is not None
        response = self.client.get("/api/users")
        assert response.status_code == 200

    def test_example(self):
        # Insert user
        response = self.client.post(
            "/api/users/add",
            content_type='application/json',
            data=json.dumps({"name": "Brett"}))
        assert response.status_code == 200
        # Insert chore
        response = self.client.post(
            "/api/chores/add",
            content_type='application/json',
            data=json.dumps({
                "name": "Fill Water",
                "description": "Fill water container in the fridge"}))
        
        assert response.status_code == 200
