import os
import main
import unittest
import tempfile
import json


class SubmitTestCase(unittest.TestCase):

    def setUp(self):
        main.app.config.from_object("config.TestingConfig")
        self.app = main.app.test_client()

        self.valid_submission = {
            "pickup_address": "123 elm ave",
            "hospital": "memorial"
        }

    def tearDown(self):
        pass

    def test_valid_response_returns_ok(self):
        rv = self.app.post("incidents", data=self.valid_submission)

        assert rv.status_code == 200
        assert json.loads(rv.data).get("status") == "ok"

    def test_response_with_empty_address_returns_error(self):
        empty_address_submission = {
            "pickup_address": ""
        }

        rv = self.app.post("incidents", data=empty_address_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "empty_address" in rv_dict.get("errors")

    def test_response_without_hospital_returns_error(self):
        missing_hospital_submission = self.valid_submission.copy()

        del missing_hospital_submission["hospital"]

        rv = self.app.post("incidents", data=missing_hospital_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "missing_hospital" in rv_dict.get("errors")

if __name__ == '__main__':
    unittest.main()