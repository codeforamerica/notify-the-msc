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
            "address": "123 elm ave"
        }

    def tearDown(self):
        pass

    def test_valid_response_returns_ok(self):
        rv = self.app.post("incidents", data=self.valid_submission )

        assert rv.status_code == 200
        assert json.loads(rv.data).get("status") == "ok"


if __name__ == '__main__':
    unittest.main()