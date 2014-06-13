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
            "language": "Khmer",
            "clothing_description": "White T-shirt, gray jeans, Nike tennis shoes",
            "interested": "No",
            "homeless": "Yes",
            "superutilizer": "Yes"
        }

    def tearDown(self):
        pass

    def test_valid_response_returns_ok(self):
        rv = self.app.post("incidents", data=self.valid_submission)

        assert rv.status_code == 200
        assert json.loads(rv.data).get("status") == "ok"

    def test_response_without_address_returns_error(self):
        missing_address_submission = {
            "pickup_address": ''
        }

        rv = self.app.post("incidents", data=missing_address_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "missing_address" in rv_dict.get("errors")

    def test_response_without_hospital_returns_error(self):
        missing_hospital_submission = self.valid_submission.copy()

        del missing_hospital_submission["hospital"]

        rv = self.app.post("incidents", data=missing_hospital_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "missing_hospital" in rv_dict.get("errors")

    def test_response_without_language_returns_error(self):
        missing_language_submission = self.valid_submission.copy()

        del missing_language_submission["language"]

        rv = self.app.post("incidents", data=missing_language_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "missing_language" in rv_dict.get("errors")

    def test_response_with_overlong_clothing_description_returns_error(self):
        overlong_clothing_description_submission = self.valid_submission.copy()

        overlong_clothing_description_submission["clothing_description"] = "White T-shirt with blue logo, gray jeans, Nike tennis shoes"

        rv = self.app.post("incidents", data=overlong_clothing_description_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "overlong_clothing_description" in rv_dict.get("errors")

    def test_response_without_clothing_description_returns_error(self):
        missing_clothing_description_submission = self.valid_submission.copy()

        del missing_clothing_description_submission["clothing_description"]

        rv = self.app.post("incidents", data=missing_clothing_description_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "missing_clothing_description" in rv_dict.get("errors")

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

    def test_response_without_superutilizer_returns_error(self):
        missing_superutilizer_submission = self.valid_submission.copy()

        del missing_superutilizer_submission["superutilizer"]

        rv = self.app.post("incidents", data=missing_superutilizer_submission)
        rv_dict = json.loads(rv.data)

        assert rv.status_code == 400
        assert rv_dict.get("status") == "error"
        assert "missing_superutilizer" in rv_dict.get("errors")

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

