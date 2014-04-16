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
            "hospital": "memorial",
            "interested": "No",
            "homeless": "Yes"
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

    def test_response_without_interested_returns_error(self):
        missing_interested_submission = self.valid_submission.copy()

        del missing_interested_submission["interested"]

        rv = self.app.post("incidents", data=missing_interested_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "missing_interested" in rv_dict.get("errors")

    def test_response_without_homeless_returns_error(self):
        missing_homeless_submission = self.valid_submission.copy()

        del missing_homeless_submission["homeless"]

        rv = self.app.post("incidents", data=missing_homeless_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "missing_homeless" in rv_dict.get("errors")

class EmailTestCase(unittest.TestCase):
    def setUp(self):
        main.app.config.from_object("config.TestingConfig")
        self.app = main.app.test_client()

        self.valid_incident = {
            "pickup_address": "123 elm ave",
            "hospital": "Memorial",
            "interested": "No",
            "homeless": "Yes",
            "clothing": "pink polo",
            "language": "English"
        }

    def tearDown(self):
        pass

    def test_build_email_from_incident_generates_html_and_text(self):
        emails = main.build_email_from_incident(self.valid_incident)

        self.assertIn('text', emails)
        self.assertIn('html', emails)

    def test_text_email_contains_all_required_info(self):
        emails = main.build_email_from_incident(self.valid_incident)

        self.assertIn('123 elm ave', emails['text'])
        self.assertIn('Memorial', emails['text'])
        self.assertIn('No', emails['text'])
        self.assertIn('Yes', emails['text'])
        self.assertIn('pink polo', emails['text'])
        self.assertIn('English', emails['text'])

    def test_html_email_contains_all_required_info(self):
        emails = main.build_email_from_incident(self.valid_incident)

        self.assertIn('123 elm ave', emails['html'])
        self.assertIn('Memorial', emails['html'])
        self.assertIn('No', emails['html'])
        self.assertIn('Yes', emails['html'])
        self.assertIn('pink polo', emails['html'])
        self.assertIn('English', emails['html'])

if __name__ == '__main__':
    unittest.main()
