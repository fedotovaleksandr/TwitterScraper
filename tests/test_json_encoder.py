from datetime import datetime
import unittest
from services.json_encoder import ApiJSONEncoder, IJSONSerializable

expected_val = 'expected_val'


class TestJSONSerializable(IJSONSerializable):
    def to_json(self):
        return expected_val


class ApiJSONEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = ApiJSONEncoder()

    def test_date(self):
        date = datetime.utcfromtimestamp(1537134063)
        actual_date = self.encoder.default(date)
        self.assertEqual(date.strftime("%I:%M - %d %b %y"), actual_date)

    def test_serializable(self):
        actual_val = self.encoder.default(TestJSONSerializable())
        self.assertEqual(expected_val, actual_val)
