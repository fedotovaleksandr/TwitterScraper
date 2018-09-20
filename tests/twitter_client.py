import unittest
from unittest.mock import patch, Mock, MagicMock

from requests import Response

from services.twitter_client import TwitterClient

expected_path = 'expected_path'
expected_params = {}
expected_headers = {}


class TwitterClientTestCase(unittest.TestCase):
    def setUp(self):
        (self.client, self.requests) = self.create_client()

    def create_client(self):
        requests = Mock()
        requests.get = MagicMock(return_value=Response())
        return TwitterClient(requests), requests

    def test_get(self):
        self.client.get(expected_path, expected_params, expected_headers)
        self.requests.get.assert_called_once_with(
            'https://twitter.com%s' % expected_path,
            params=expected_params,
            headers=expected_headers
        )
